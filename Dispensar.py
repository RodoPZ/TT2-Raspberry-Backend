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
primaryColor = "#f85f6a"
ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
def Dispensar(dosisVar,pastillasVar,horaVar,repetirVar,dosisId,seguridadVar):
    
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
        pillNameList.insert(n,data[pill[0]]["nombre"])
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
        pload = []
        Value = data[seguridadVar]["uid"]
        if(Nfc.reconocer(Value,ser)):
            for i in pastillasVar:
                pload.append([pill[0],data[pill[0]]["contenedor"],i[1],repetirVar,dosisId])
            print(pload)
            r = requests.post('http://localhost:8080/Dispensar',data = json.dumps(pload))
            print(r.text)
            root.destroy()
        else:
            ser.write(b'6')
            time.sleep(3)
            ser.write(b'E')

    def DispensarFacial():
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
                pload.append([pill[0],data[pill[0]]["contenedor"],i[1],repetirVar,dosisId])
            print(pload)
            r = requests.post('http://localhost:8080/Dispensar',data = json.dumps(pload))
            print(r.text)
            root.destroy()
        else:
            print("Error")


    def DispensarPin():
        pload = []
        if(data[seguridadVar]["pinData"] == PINentry1.get()):

            for i in pastillasVar:
                pload.append([pill[0],data[pill[0]]["contenedor"],i[1],repetirVar,dosisId])
            print(pload)
            r = requests.post('http://localhost:8080/Dispensar',data = json.dumps(pload))
            print(r.text)
            root.destroy()
        else:
            ErrorText = tkinter.Label(root,text='Error',fg="red")
            ErrorText.configure(font=("Asap",20))
            ErrorText.grid(row=11,column=0,columnspan=4)

            


    if(data[seguridadVar]["tipo"] == "NFC"):
        Label2 = tkinter.Label(root,text='Presione el botón de "Dispensar" y coloque su tarjeta RFID en el recuadro blanco frente al dispensador')
        Label2.configure(font=("Asap",20))
        Label2.grid(row=8,column=0,columnspan=4)

        button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarNFC)
        button1.grid(row=9,column=0,columnspan=4)  

    if(data[seguridadVar]["tipo"] == "RECONOCIMIENTO FACIAL"):
        Label2 = tkinter.Label(root,text='Presione el botón de "Dispensar" y colóquese frente al dispensador hasta que se reconozca su rostro')
        Label2.configure(font=("Asap",20))
        Label2.grid(row=8,column=0,columnspan=4)

        button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=DispensarFacial)
        button1.grid(row=9,column=0,columnspan=4)

    if(data[seguridadVar]["tipo"] == "PIN"):
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
        
    root.mainloop()

if __name__ == "__main__":
    Dispensar("Dosis1",[["hkyy46ipUqojrwuXjCjM",1]],"10:20","Una Vez","1cn6zVd0BjQ0O7240qSs","vO1vpJwvCHiKmdmwno72")
