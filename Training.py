import cv2
import os
import numpy as np

def train(fileName):
	personName = fileName[:fileName.index(".")]
	dataPath = 'Data'
	labels = []
	facesData = []
	label = 0

	personPath = dataPath + '/' + personName
	print('Leyendo las imágenes')

	for imgName in os.listdir(personPath):
		print('Rostros: ', personName + '/' + imgName)
		labels.append(label)
		facesData.append(cv2.imread(personPath+'/'+imgName,0))
	label += 1

	# Métodos para entrenar el reconocedor
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	face_recognizer.train(facesData, np.array(labels))
	face_recognizer.write(fileName)

	return "ok"
