import tkinter
import json    
import requests
import os
import time
import Face
import Nfc
import Storage
import serial
primaryColor = "#f85f6a"
#ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)

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

    Label6 = tkinter.Label(root,text='Presione "Dispensar" para iniciar la dispensación')
    Label6.configure(font=("Asap",15))
    Label6.grid(row=8,column=0,columnspan=4)

    def command():
        pload = []
        if(seguridadVar != ""):
            seguridad = data[seguridadVar]
            if(seguridad["tipo"]=="RECONOCIMIENTO FACIAL"):
                fileName = seguridad["nombre"]+".xml" #Comunicación desde APP a Python
                
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

            if(seguridad["tipo"]=="NFC"):
                Value = seguridad["uid"]
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
                

    button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=command)
    button1.grid(row=9,column=0,columnspan=4)
    
    
    root.mainloop()

if __name__ == "__main__":
    Dispensar("Dosis1",[["kLeJ7nutkFt8TX5aMA4c",1]],"10:20","Una Vez","fof5a1ccKYm9Jc5278o0","l1seFWPSiy9XtjhXFk6W")
