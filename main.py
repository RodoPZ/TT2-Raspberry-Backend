from fileinput import filename
from socket import timeout
from time import sleep
from bottle import route, run, response, get, post, request, HTTPResponse
from FaceCapture import capture
from Training import train
from FaceRecognition import recognize
from Storage import *
import os.path
import json
import serial,time

ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 1)
sleep(2)
ser.write(b'P')

@post('/RegisterFace')
def RegisterFace():
    fileName = request.body.getvalue().decode('utf-8') + ".xml" #Comunicación desde APP a Python
    sleep(1)
    if os.path.exists(fileName):
        recognize(fileName)
        return HTTPResponse(body="False")
    else:
        if checkModel(fileName) == False:
            print("No existe modelo")
            capture(fileName)
            train(fileName)
            uploadFile(fileName)
            print("awa")
    return HTTPResponse(body="True") #Comunicación desde Python a APP
    
@post('/DeleteFace')
def DeleteFace():
    fileName = request.body.getvalue().decode('utf-8') + ".xml" 
    print(fileName)
    sleep(1)
    if os.path.exists(fileName):
        os.remove(fileName)
    if checkModel(fileName):
        delete(fileName)
        
    return HTTPResponse(body=True)

@post('/RegisterNfc')
def RegisterNfc():
    texto = ""
    fileName = request.body.getvalue().decode('utf-8') 
    ser.write(b'1')
    ser.write(b'0')
    cont = 0
    ser.flushInput()
    while True:
        cont+= 1
        ard=ser.readline()
        if(str(ard).startswith("b'UID:")):
            texto = str(ard).split(": ")[1]
            texto = str(texto).split("\\")[0]
            UID = texto
            break
        print(ard)
        sleep(1)
    #Ejecutar aqui todo lo necesario para reconocer mediante NFC y obtener el UID
    print(UID)
    return HTTPResponse(UID)    #regresar el UID

run(host='localhost', port=8080, debug=True)
