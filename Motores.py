from time import sleep

def dispensar(cantidad,compartimento, numero, ser):
	ser.flushInput()
	ser.write(b'2')
	ard=ser.readline()
	print(ard)        
	
	sleep(3)
	ser.flushInput()
	ser.write(b'8')
	ard=ser.readline()
	print(ard)        
	sleep(2)
	ser.write(cantidad.encode('UTF-8'))
	ard=ser.readline()
	print(ard)
	sleep(2)
	ser.write(compartimento.encode('UTF-8'))            
	ard=ser.readline()
	print(ard)
	sleep(2)
	ser.write(numero.encode('UTF-8'))
	print(ard)
	
def mover(compartimento,ser):
	sleep(1)
	ser.flushInput()
	ser.write(b'2')
	sleep(1)
	ser.write(b'9')
	sleep(2)
	ser.write(compartimento.encode('UTF-8'))

