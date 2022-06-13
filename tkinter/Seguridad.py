import tkinter
from tkinter import *
import serial
from numpy import size
primaryColor = "#f85f6a"
ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)



def Seguridad(metodoSeguridad,pin):

    root=tkinter.Tk()
    root.title("Dispensar")

    Label1 = tkinter.Label(root,text='Dispensando')
    Label1.configure(font=("Asap",20))
    Label1.grid(row=0,column=0,columnspan=4)

    if(metodoSeguridad == "NFC"):
        Label2 = tkinter.Label(root,text='Coloque su tarjeta RFID en el recuadro blanco frente al dispensador')
        Label2.configure(font=("Asap",20))
        Label2.grid(row=1,column=0,columnspan=4)

        button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=validate,height=1)
        button1.grid(row=5,column=0,columnspan=4)

    if(metodoSeguridad == "RECONOCIMIENTO FACIAL"):
        Label2 = tkinter.Label(root,text='Colóquese frente al dispensador hasta que se reconozca su rostro')
        Label2.configure(font=("Asap",20))
        Label2.grid(row=1,column=0,columnspan=4)

    if(metodoSeguridad == "PIN"):
        Label2 = tkinter.Label(root,text='Ingrese su PIN')
        Label2.configure(font=("Asap",20))
        Label2.grid(row=1,column=0,columnspan=4)
        frame = tkinter.Frame(root,height=20)
        frame.grid(row=2,column=1)

        def limitSizeDay(*args):
            value = PINentry.get()
            if len(value) > 4: PINentry.set(value[:4])

        PINentry = tkinter.StringVar()
        PINentry.trace('w', limitSizeDay)
        PINentry1=Entry(bg="white", fg="black", width=4, textvariable=PINentry,font=("Asap,20"))
        PINentry1.grid(row=3,column=0,columnspan=4,ipady=10)
        

        frame = tkinter.Frame(root,height=20)
        frame.grid(row=4,column=1)

        def validate():
            if(pin == PINentry1.get()):
                print("ok")
            

        button1=tkinter.Button(root, text="Dispensar", bg='#f85f6a',fg="white" ,font=("Asap",20),command=validate,height=1)
        button1.grid(row=5,column=0,columnspan=4)


    root.mainloop()

if __name__ == "__main__":
    Seguridad("PIN","1234")
