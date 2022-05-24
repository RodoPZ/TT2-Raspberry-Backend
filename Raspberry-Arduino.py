import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
if ser.isOpen():
	print("conectado",format(ser.port))
	try:
		while True:
			ard = ser.readline()
			print(ard)		
			if(ard == b'uwu\r\n'):
				print("ekljdfgsg")
			ser.write(b'1')
			time.sleep(1)
			
	except KeyboardInterrupt:
		print("aio chulo")
