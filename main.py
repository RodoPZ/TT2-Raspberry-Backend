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



if ser.isOpen():
    print("Conectado", format(ser.port))
    cont = 0
    while True:
        cont+= 1
        ard=ser.readline()
        print(ard)
        sleep(1)
        if cont == 5:
            break

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
    fileName = request.body.getvalue().decode('utf-8') 
    cont = 0
    ser.write(b'P')
    while True:
        cont+= 1
        ard=ser.readline()
        print(ard)
        sleep(1)
        if cont == 5:
            break

    sleep(5)
    
    ser.write(b'1')
    receiving(ser)
    sleep(5)
    #Ejecutar aqui todo lo necesario para reconocer mediante NFC y obtener el UID
    UID = "XXXXXXXXXXXXXXXXXX"        
    return HTTPResponse(UID)    #regresar el UID

def receiving(ser):
    global last_received
    buffer_string = ''
    cont = 0
    while cont <= 5:
        cont += 1
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]
run(host='localhost', port=8080, debug=True)
