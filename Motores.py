from time import sleep

def dispensar(cantidad,compartimento, ser):
	sleep(3)
	ser.write(str(cantidad).encode())
	sleep(3)
	ser.write(str(compartimento).encode())     
	       
	
def mover(compartimento,ser):
	sleep(4)
	ser.flushInput()
	ser.write(b'2')
	sleep(4)
	ser.write(b'9')
	sleep(4)
	ser.write(str(compartimento).encode())

