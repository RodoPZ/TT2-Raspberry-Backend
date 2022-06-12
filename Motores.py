from time import sleep

def dispensar(cantidad,compartimento, numero, ser):
	sleep(2)
	ser.write(b'2')
	sleep(2)
	ser.write(b'8')
	sleep(2)
	ser.write(str(cantidad).encode())
	sleep(3)
	ser.write(str(compartimento).encode())            
	sleep(2)
	ser.write(str(numero).encode())
	ser.flushInput()
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

