from bottle import route, run, response, get, post, request, HTTPResponse
import Face
import Storage
import Dispensar
import Nfc
import os.path
import serial,time


# ~ ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
time.sleep(1)

@post('/RegisterFace')
def RegisterFace():
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
        
    if checkModel(fileName):
        delete(fileName)
        
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
    UID = Nfc.registrar()
    return HTTPResponse(UID)    #regresar el UID
    
@post('/RegisterNfc')
def RegisterNfc():
    Value = request.body.getvalue().decode('utf-8')
    Value = "29 53 59 98"
    if(Nfc.reconocer(Value)):
        ser.write(b'7')
        time.sleep(3)
        ser.write(b'E')
        return HTTPResponse("False")
    else:
        Dispensar.dispensar("1","B"," 4921709107")
        return HTTPResponse("True")
run(host='localhost', port=8080, debug=True)
