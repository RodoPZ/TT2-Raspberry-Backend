import tkinter
from tkinter import *
import serial
from numpy import size
import sys
primaryColor = "#f85f6a"

def PocasPastillas(compartimento):

    root2=tkinter.Toplevel()
    root2.title("Quedan pocas pastillas")

    Label1 = tkinter.Label(root2,text=f'Quedan pocas pastillas en el compartimento {compartimento}')
    Label1.configure(font=("Asap",20))
    Label1.grid(row=0,column=0,columnspan=4)
    button1=tkinter.Button(root2, text="ok", bg='#f85f6a',fg="white" ,font=("Asap",20),command=root2.destroy)
    button1.grid(row=2,column=0,columnspan=4)
    root2.mainloop()

if __name__ == "__main__":
    Seguridad(2)
