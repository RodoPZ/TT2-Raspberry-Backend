from bottle import route, run, response, get, post, request, HTTPResponse
from cv2 import merge
from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore
import Face
import Storage
import Motores
import Nfc
import os.path
import serial,time
import json
import requests
import Dispensar as DispensarDosis
from datetime import datetime
import subprocess

#ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
subprocess.run("lxterminal -e bash -c 'python3 Alarmas.py ; read v'", shell=True)
time.sleep(1)


@post('/RegisterFace')
def RegisterFace():
    fileName = request.body.getvalue().decode('utf-8') + ".xml" #Comunicación desde APP a Python
    time.sleep(1)
    if os.path.exists(fileName):
        return HTTPResponse(body="False")
    else:
        if Storage.checkModel(fileName) == False:
            print("No existe modelo")
            Face.capture(fileName)
            Face.train(fileName)
            Storage.uploadFile(fileName)
            print("awa")
    return HTTPResponse(body="True") #Comunicación desde Python a APP
    
@post('/DeleteFace')
def DeleteFace():
    fileName = request.body.getvalue().decode('utf-8') + ".xml" 
    print(fileName)
    time.sleep(1)
    if os.path.exists(fileName):
        os.remove(fileName)
    if Storage.checkModel(fileName):
        Storage.delete(fileName)
    return HTTPResponse(body=True)

@post('/RegisterNfc')
def RegisterNfc():
    UID = Nfc.registrar(ser)
    return HTTPResponse(UID)    #regresar el UID
    
@post('/RecognizeNfc')
def RecognizeNfc():
    Value = request.body.getvalue().decode('utf-8')
    if(Nfc.reconocer(Value,ser)):
        return HTTPResponse("True")
    else:
        ser.write(b'6')
        time.sleep(3)
        ser.write(value[0][5].encode()) 
        return HTTPResponse("False")
    
@post('/Dispensar')
def Dispensar():
    db = firestore.client()
    value = request.body.getvalue().decode('utf-8')
    value = json.loads(value)
    ser.write(b'2')
    time.sleep(2)
    ser.write(b'8')
    time.sleep(2)

    for i in value:
        cantidad = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Pastillas").document(i[0]).get()
        cantidad = cantidad.to_dict()["cantidad"]
        cantidad = cantidad - i[2]
        db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Pastillas").document(i[0]).update({"cantidad" : cantidad})
        Compartimento = chr(ord('@')+int(i[1]))
        while True:
            ard=ser.readline()
            print(ard)
            if(str(ard).startswith("b'Ingrese la dosis")):
                time.sleep(2)
                Motores.dispensar(i[2],Compartimento,ser)
                break 
    while True:
        ard=ser.readline()
        print(ard)
        if(str(ard).startswith("b'Ingrese la dosis")):
            break 
    time.sleep(2)
    ser.write(b'1')
    time.sleep(2)
    ser.write(b'K')
    time.sleep(2)
    ser.write(value[0][5].encode())  
    while True:
        ard=ser.readline()
        print(ard)
        if(str(ard).startswith("b'OK")):
            break 

    if(i[3] == "Una vez"):
        db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").document(i[4]).update({"horario" : ""})
    db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").document(i[4]).set({"historial" : {str(datetime.today())[:16]:"True"}},merge=True)
    return HTTPResponse("True")
     

@post('/MoverMotores')
def MoverMotores():
    value = request.body.getvalue().decode('utf-8')
    value = chr(ord('@')+int(value))
    Motores.mover(value,ser)
    return HTTPResponse("True")

@post('/OpenDispensar')
def OpenDispensar():
    value = request.body.getvalue().decode('utf-8')
    
    value= json.loads(value)
    print(value)
    name = value[0]
    pills = json.loads(value[1])
    hourmin = value[2]
    alarm_repetir = value[3]
    dosis_Id = value[4]
    dosis_Seguridad = value[5]
    numstring = value[6]
    DispensarDosis.Dispensar(name,pills,hourmin,alarm_repetir,dosis_Id,dosis_Seguridad,numstring)
    return HTTPResponse("True")

run(host='localhost', port=8080, debug=True)
