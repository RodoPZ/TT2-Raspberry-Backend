from time import sleep

def dispensar(cantidad,compartimento, numero, ser):
	sleep(5)
	ard=ser.readline()
	ser.flushInput()
	ser.write(b'2')
	ard=ser.readline()
	print(ard)        
	sleep(4)

	ser.flushInput()
	ser.write(b'8')
	ard=ser.readline()
	print(ard)
	sleep(3)
	
	ser.write(str(cantidad).encode())
	ard=ser.readline()
	print(ard)
	sleep(3)

	ser.write(str(compartimento).encode())            
	ard=ser.readline()
	print(ard)
	sleep(3)

	ser.write(str(numero).encode())
	ard=ser.readline()
	print(ard)
	while True:
		ard=ser.readline()
		print(ard)
		if(str(ard).startswith("b'Inicio")):
			break
	sleep(5)
	
	
def mover(compartimento,ser):
	sleep(3)
	ser.flushInput()
	ser.write(b'2')
	sleep(3)
	ser.write(b'9')
	sleep(3)
	ser.write(str(compartimento).encode())

