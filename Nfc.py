from  time import sleep
def reconocer(nfcReconocer,ser):
	i = 0
	ser.write(b'2')
	ser.flushInput()
	while True:
		ard=ser.readline()
		if(str(ard).startswith("b'UID:")):
			texto = str(ard).split(": ")[1]
			texto = str(texto).split("\\")[0]
			UID = texto
			print(UID)
			if(UID == nfcReconocer):
				return True
			else:
				i+=1
		if(i == 3):
			return False

		print(ard)
		
		
def registrar(ser):
	texto = ""
	ser.write(b'1')
	ser.write(b'0')
	ser.flushInput()
	while True:
		ard=ser.readline()
		if(str(ard).startswith("b'UID:")):
			texto = str(ard).split(": ")[1]
			texto = str(texto).split("\\")[0]
			UID = texto
			print(UID)
			return UID
		print(ard)
		sleep(1)
