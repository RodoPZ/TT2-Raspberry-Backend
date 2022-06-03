from bottle import route, run, response, get, post, request, HTTPResponse
import Face
import Storage
import Motores
import Nfc
import os.path
import serial,time
import json
import requests
#ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
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

@post('/RecognizeFace')
def RecognizeFace():
    fileName = request.body.getvalue().decode('utf-8') + ".xml" #Comunicación desde APP a Python
    print(fileName)
    time.sleep(1) 
    if os.path.exists(fileName):
        Face.recognize(fileName)
    elif Storage.checkModel(fileName):
        Storage.download(filename)
        Face.recognize(fileName)
    else:
        print("Error: No existe el modelo")
    return HTTPResponse(body=True)
    
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
    Value = "29 53 59 98"
    if(Nfc.reconocer(Value,ser)):
        return HTTPResponse("True")
    else:
        ser.write(b'6')
        time.sleep(3)
        ser.write(b'E')
        return HTTPResponse("False")
    
@post('/Dispensar')
def Dispensar():
    value = request.body.getvalue().decode('utf-8')
    value = json.loads(value)
    for i in value:
        print(i)
    # Motores.dispensar("1","B", " 4921442910",ser)
    return HTTPResponse("True")
     

@post('/MoverMotores')
def MoverMotores():
    value = request.body.getvalue().decode('utf-8')
    print(value)
    value = chr(ord('@')+int(value))
    print(value)
    Motores.mover(value,ser)
    return HTTPResponse("True")

run(host='localhost', port=8080, debug=True)
