from fileinput import filename
from time import sleep
from bottle import route, run, response, get, post, request
from FaceCapture import capture
from Training import train
from FaceRecognition import recognize
from Storage import *
import os.path

@post('/')
def hello():
    fileName = request.body.getvalue().decode('utf-8') + ".xml"

    sleep(2)
    if os.path.exists(fileName):
        if checkModel(fileName):
            recognize(fileName)
        else:
            recognize(fileName)
            uploadFile(fileName) 
    else:
        if checkModel(fileName):
            print("ya existe modelo")
            download(fileName)
            recognize(fileName)
        else:
            print("No existe modelo")
            capture(fileName)
            train(fileName)
            recognize(fileName)
            uploadFile(fileName)
    return "ok"
    
run(host='192.168.0.11', port=8080, debug=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name




