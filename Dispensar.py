import tkinter
from tkinter import *
import json
import requests
import os
import time
import Face
import Nfc
import Storage
import serial
import Motores
import PocasPastillas   
from datetime import datetime
from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore

primaryColor = "#f85f6a"
Dispensado = False
ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
error = 0



def Dispensador(value):
    global Dispensado
    with open('data.json') as json_file:
        data = json.load(json_file)
    pocasPastillas = False
    db = firestore.client()
    value = json.loads(value)
    print("awa " + str(value))
    ser.write(b'2')
    time.sleep(2)
    ser.write(b'8')
    time.sleep(2)
    for i in value:
        print(i)
        cantidad = data["pastillas"][i[0]]["cantidad"]
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
    time.sleep(4)
    ser.write(value[0][5].encode())  
    time.sleep(3)
    while True:
        ard=ser.readline()
        print(ard)
        if(str(ard).startswith("b'OK")):
            break 

    if(value[0][3] == "Una vez"):
        db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").document(value[0][4]).update({"horario" : ""})
    db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").document(value[0][4]).set({"historial" : {str(datetime.today())[:10]:str(datetime.today())[10:16]}},merge=True)
    for i in value:
        if data["pastillas"][i[0]]["cantidad"]<6:
            time.sleep(3)
            ser.write(b'3')
            time.sleep(3)
            ser.write(value[0][5].encode()) 
            time.sleep(3)
            while True:
                ard=ser.readline()
                print(ard)
                if(str(ard).startswith("b'OK")):
                    break   
    Dispensado = True

            
def Dispensar(dosisVar,pastillasVar,horaVar,repetirVar,dosisId,seguridadVar,contactosList):
    global Dispensado
    global error
    Dispensado = False
    with open('data.json') as json_file:
        data = json.load(json_file)
    root=tkinter.Tk()
    root.title("Dispensar")

    #root.attributes('-fullscreen',True)

    Label1 = tkinter.Label(root,text='Es hora de su dosis')
    Label1.configure(font=("Asap",20))
    Label1.grid(row=0,column=0,columnspan=4)

    #frame
    frame = tkinter.Frame(root,height=20)
    frame.grid(row=1,column=1)
    #Dosis
    dosisLabel = tkinter.Label(root,text=f'Dosis: ')
    dosisLabel.configure(font=("Asap",15))
    dosisLabel.grid(row=2,column=1)
    dosisVarLabel = tkinter.Label(root,text=dosisVar,fg=primaryColor)
    dosisVarLabel.configure(font=("Asap",15))
    dosisVarLabel.grid(row=2,column=2)

    #Pastillas
    pastillasLabel = tkinter.Label(root,text=f'Pastillas')
    pastillasLabel.configure(font=("Asap",15))
    pastillasLabel.grid(row=3,column=1)
  
    pastillasVarLabel = tkinter.Label(root,text="Cantidad")
    pastillasVarLabel.configure(font=("Asap",15))
    pastillasVarLabel.grid(row=3,column=2)

    pillNameList = tkinter.Listbox(height=len(pastillasVar),justify=tkinter.CENTER)
    for n,pill in enumerate(pastillasVar):
        pillNameList.insert(n,data["pastillas"][pill[0]]["nombre"])
    pillNameList.config(state=tkinter.DISABLED)
    pillNameList.grid(row=4,column=1,columnspan=1)

    pillItemList = tkinter.Listbox(height=len(pastillasVar),width=2,justify=tkinter.CENTER)
    for n,pill in enumerate(pastillasVar):
        print(pill)
        pillItemList.insert(n,pill[1])
    pillItemList.config(state=tkinter.DISABLED)
    pillItemList.grid(row=4,column=2,columnspan=1)

    #Hora
    horaLabel = tkinter.Label(root,text=f'Hora: ')
    horaLabel.configure(font=("Asap",15))
    horaLabel.grid(row=5,column=1)
    horaVarLabel = tkinter.Label(root,text=horaVar,fg=primaryColor)
    horaVarLabel.configure(font=("Asap",15))
    horaVarLabel.grid(row=5,column=2)

    #Repetir
    repetirLabel = tkinter.Label(root,text=f'Se repite:')
    repetirLabel.configure(font=("Asap",15))
    repetirLabel.grid(row=6,column=1)
    repetirVarLabel = tkinter.Label(root,text=repetirVar,fg=primaryColor)
    repetirVarLabel.configure(font=("Asap",15))
    repetirVarLabel.grid(row=6,column=2)

    #frame
    frame = tkinter.Frame(root,height=20)
    frame.grid(row=7,column=1)

    def DispensarNFC():
        ser.write(b'E')
        time.sleep(5)
        pload = []
        Value = data[seguridadVar]["uid"]
        if(Nfc.reconocer(Value,ser)):
            for i in pastillasVar:
                pload.append([i[0],data["pastillas"][i[0]]["contenedor"],i[1],repetirVar,dosisId,contactosList])
            print(pload)
            Dispensador(json.dumps(pload))
            root.destroy()
        else:
            ser.write(b'6')
            time.sleep(3)
            ser.write(str(contactosList).encode())
            while True:
                ard=ser.readline()
                print(ard)
                if(str(ard).startswith("b'OK")):
                    break 


    def DispensarFacial():
        ser.write(b'E')
        time.sleep(5)
        pload = []
        fileName = data[seguridadVar]["nombre"]+".xml" #Comunicación desde APP a Python
        time.sleep(1) 
        if os.path.exists(fileName):
            print(fileName)
            verificado = Face.recognize(fileName)
        elif Storage.checkModel(fileName):
            Storage.download(fileName)
            verificado = Face.recognize(fileName)
        else:
            print("Error: No existe el modelo")

        if(verificado == True):
            for i in pastillasVar:
                pload.append([i[0],data["pastillas"][i[0]]["contenedor"],i[1],repetirVar,dosisId,contactosList])
            print(pload)
            Dispensador(json.dumps(pload))
            root.destroy()
        else:
            ser.write(b'2')
            time.sleep(3)
            ser.write(b'6')
            time.sleep(3)
            ser.write(str(contactosList).encode())
            while True:
                ard=ser.readline()
                print(ard)
                if(str(ard).startswith("b'OK")):
                    break 

    def DispensarPin():
        ser.write(b'E')
        time.sleep(5)
        global error
        pload = []
        if(data[seguridadVar]["pinData"] == PINentry1.get()):
            for i in pastillasVar:
                pload.append([i[0],data["pastillas"][i[0]]["contenedor"],i[1],repetirVar,dosisId,contactosList])
            print(pload)
            Dispensador(json.dumps(pload))
            root.destroy()
        else:
            error+=1
            print(error)
            if error == 3: 
                error = 0 
                ser.write(b'2')
                time.sleep(3)
                ser.write(b'6')
                time.sleep(4)    
                ser.write(str(contactosList).encode())
                while True:
                    ard=ser.readline()
                    print(ard)
                    if(str(ard).startswith("b'OK")):
                        break 
            else:
                ErrorText = tkinter.Label(root,text='Error',fg="red")
                ErrorText.configure(font=("Asap",20))
                ErrorText.grid(row=11,column=0,columnspan=4)

    def DispensarNoSeguridad():
        ser.write(b'E')
        time.sleep(5)
        pload = []
        for i in pastillasVar:
            pload.append([i[0],data["pastillas"][i[0]]["contenedor"],i[1],repetirVar,dosisId,contactosList])
        print("Enviar: " + str(pload))
        Dispensador(json.dumps(pload))
        root.destroy()

    if(seguridadVar!=""):
        if(data[seguridadVar]["tipo"] == "NFC"):
            Label2 = tkinter.Label(root,text='Presione el botón de "Dispensar" \n y coloque su tarjeta RFID en el recuadro \n blanco frente al dispensador')
            Label2.configure(font=("Asap",14))
            Label2.grid(row=8,column=0,columnspan=4)

            button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarNFC)
            button1.grid(row=9,column=0,columnspan=4)  

        elif(data[seguridadVar]["tipo"] == "RECONOCIMIENTO FACIAL"):
            Label2 = tkinter.Label(root,text='Presione el botón de "Dispensar" \n y colóquese frente al dispensador \n hasta que se reconozca su rostro')
            Label2.configure(font=("Asap",14))
            Label2.grid(row=8,column=0,columnspan=4)

            button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarFacial)
            button1.grid(row=9,column=0,columnspan=4)

        elif(data[seguridadVar]["tipo"] == "PIN"):
            Label2 = tkinter.Label(root,text='Ingrese su PIN')
            Label2.configure(font=("Asap",20))
            Label2.grid(row=8,column=0,columnspan=4)
            frame = tkinter.Frame(root,height=10)
            frame.grid(row=9,column=1)

            def limitSizeDay(*args):
                value = PINentry.get()
                if len(value) > 4: PINentry.set(value[:4])

            PINentry = tkinter.StringVar()
            PINentry.trace('w', limitSizeDay)
            PINentry1=Entry(bg="white", fg="black", width=4, textvariable=PINentry,font=("Asap,20"))
            PINentry1.grid(row=10,column=0,columnspan=4,ipady=10)
            
            frame = tkinter.Frame(root,height=10)
            frame.grid(row=11,column=1)
            button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarPin)
            button1.grid(row=12,column=0,columnspan=4)
    else:
        button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarNoSeguridad)
        button1.grid(row=12,column=0,columnspan=4)
    root.mainloop()
    return Dispensado

if __name__ == "__main__":
    Dispensar("Dosis1",[["UiTv2t7F3IHvwiLExqaH",1]],"10:20","Una Vez","1cn6zVd0BjQ0O7240qSs","","0")
