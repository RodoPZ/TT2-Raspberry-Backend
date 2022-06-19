import tkinter
from tkinter import *
import serial
from numpy import size
primaryColor = "#f85f6a"

def PocasPastillas(compartimento):

    root=tkinter.Tk()
    root.title("Dispensar")

    Label1 = tkinter.Label(root,text=f'Quedan pocas pastillas en el compartimento {compartimento}')
    Label1.configure(font=("Asap",20))
    Label1.grid(row=0,column=0,columnspan=4)
    button1=tkinter.Button(root, text="ok", bg='#f85f6a',fg="white" ,font=("Asap",20),command=root.destroy)
    button1.grid(row=2,column=0,columnspan=4)
    root.mainloop()

if __name__ == "__main__":
    Seguridad(2)
