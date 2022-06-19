import tkinter
from tkinter import *
import serial
from numpy import size
primaryColor = "#f85f6a"

def Seguridad(name,days,date):

    root=tkinter.Tk()
    root.title("Dispensar")

    Label1 = tkinter.Label(root,text=f'Sus pastillas de {name} se caducan dentro de {days} días')
    Label1.configure(font=("Asap",20))
    Label1.grid(row=0,column=0,columnspan=4)
    Label2 = tkinter.Label(root,text=f'Caducidad: {date}')
    Label2.configure(font=("Asap",20))
    Label2.grid(row=1,column=0,columnspan=4)
    button1=tkinter.Button(root, text="ok", bg='#f85f6a',fg="white" ,font=("Asap",20),command=root.destroy)
    button1.grid(row=2,column=0,columnspan=4)
    root.mainloop()

if __name__ == "__main__":
    Seguridad("Paracetamol",3,"10/10/2022")
