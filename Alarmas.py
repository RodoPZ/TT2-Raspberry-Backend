
from ast import While
from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore
import datetime
import time
import ActualizarAlarmas
cred = credentials.Certificate("tt2-database-31516e0b99db.json") #descargar de https://console.cloud.google.com/iam-admin/serviceaccounts/details/101070432244239069365/keys?project=tt2-database
initialize_app(cred, {'storageBucket': 'tt2-database.appspot.com'})
db = firestore.client()
collection = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").get()
Dosis = []

while(True):
    for doc in collection:
        for horaid in doc.to_dict()["horario"]:
            alarm_day = []
            hora = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Horarios").document(horaid).get()
            if(hora.to_dict()["repetir"] == "Diariamente"):
                alarm_day = [1,2,3,4,5,6,7]
            elif(hora.to_dict()["repetir"] == "Una vez"):
                alarm_day = current_min = datetime.datetime.now().strftime("%D") #cambiar
            elif(hora.to_dict()["repetir"] == "Lun a Vie"):
                alarm_day = [1,2,3,4,5]
            else:
                for day in hora.to_dict()["repetir"]:
                    if(day == "Lu"):
                        alarm_day.append(1)
                    if(day == "Ma"):
                        alarm_day.append(2)
                    if(day == "Mi"):
                        alarm_day.append(3)
                    if(day == "Ju"):
                        alarm_day.append(4)
                    if(day == "Vi"):
                        alarm_day.append(5)
                    if(day == "Sa"):
                        alarm_day.append(6)
                    if(day == "Do"):
                        alarm_day.append(7)
            alarm_hour = hora.to_dict()["hora"][0:2]
            alarm_min = hora.to_dict()["hora"][3:5]
            Dosis.append([alarm_day,alarm_hour,alarm_min,doc.id])
    ActualizarAlarmas.setAlarm(Dosis)
                




