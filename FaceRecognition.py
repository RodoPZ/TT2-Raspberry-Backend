from itertools import count
import cv2
import os

def recognize(fileName):
	dataPath = 'Data' 
	imagePaths = os.listdir(dataPath)
	print("Iniciando reconocimiento")
	reconocido = False
	window_name = "frame"
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	# Leyendo el modelo

	face_recognizer.read(fileName)

	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	cap.set(3, 1280)
	cap.set(4, 720)
	#cap = cv2.VideoCapture('Resources/Video-mujer-frente.mp4')
	#cap = cv2.VideoCapture('Resources/Video-rostros.mp4')

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	while True:
		ret, frame = cap.read()
		frame = cv2.convertScaleAbs(frame, alpha = 1, beta = 255*0.05)
		if ret == False: break
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = gray.copy()

		faces = faceClassif.detectMultiScale(gray,1.3,5)

		for (x,y,w,h) in faces:
			rostro = auxFrame[y:y+h,x:x+w]
			rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
			result = face_recognizer.predict(rostro)

			cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

			if result[1] < 70:
				cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				print("reconocido")
				reconocido = True
			else:
				cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
		
		cv2.imshow(window_name,frame)
		k = cv2.waitKey(1)
		if k == 27 or reconocido == True:
			break

	cap.release()
	cv2.destroyAllWindows()