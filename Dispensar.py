def dispensar(cantidad,compartimento, numero):
	sleep(1)
	ser.flushInput()
	ser.write(b'5')
	ard=ser.readline()
	print(ard)        
	sleep(1)
	ser.write(cantidad.encode('UTF-8'))
	ard=ser.readline()
	print(ard)
	sleep(1)
	ser.write(compartimento.encode('UTF-8'))            
	ard=ser.readline()
	print(ard)
	sleep(2)
	ser.write(numero.encode('UTF-8'))
	print(ard)
