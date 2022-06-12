from xmlrpc.client import DateTime
from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore
from datetime import datetime, timedelta
import time
import json
import ActualizarAlarmas
import requests

def withNoInternet():
    Dosis = []
    with open('data.json') as json_file:
        data = json.load(json_file)
    while(True):
        time.sleep(1)
        if(len(Dosis) != len(data["dosis"])):
            for doc in data["dosis"]:
                for horaid in doc["horario"]:
                    alarm_day = []
                    hora = data[horaid]
                    if(hora["repetir"] == "Diariamente"):
                        alarm_day = [1,2,3,4,5,6,7]
                    elif(hora["repetir"] == "Una vez"):
                        alarm_day = current_min = datetime.datetime.now().strftime("%D") #cambiar
                    elif(hora["repetir"] == "Lun a Vie"):
                        alarm_day = [1,2,3,4,5]
                    else:
                        for day in hora["repetir"]:
                            if(day == "Lu"):
                                alarm_day.append(0)
                            if(day == "Ma"):
                                alarm_day.append(1)
                            if(day == "Mi"):
                                alarm_day.append(2)
                            if(day == "Ju"):
                                alarm_day.append(3)
                            if(day == "Vi"):
                                alarm_day.append(4)
                            if(day == "Sa"):
                                alarm_day.append(5)
                            if(day == "Do"):
                                alarm_day.append(6)
                    alarm_hour = hora["hora"][0:2]
                    alarm_min = hora["hora"][3:5]
                    Dosis.append([alarm_day,alarm_hour,alarm_min])        
        ActualizarAlarmas.setAlarm(Dosis)

def withInternet():
    cred = credentials.Certificate("tt2-database-31516e0b99db.json") #descargar de https://console.cloud.google.com/iam-admin/serviceaccounts/details/101070432244239069365/keys?project=tt2-database
    initialize_app(cred, {'storageBucket': 'tt2-database.appspot.com'})
    db = firestore.client()
    Ids = []
    Dosis = []
    while(True):
        dosisdata = []
        data = {}
        collection = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").get()
        time.sleep(3)
        if(collection != Ids and str(collection)!="[]"):
            Ids = collection
            for doc in collection:
                doc = doc.to_dict()
                dosisdata.append(doc)

                for PastillaList in json.loads(doc["pastillas"]):
                    print(PastillaList)
                    pastillaid = PastillaList[0]
                    pastilladata = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Pastillas").document(pastillaid).get()
                    data.update({pastillaid : pastilladata.to_dict()})

                alarm_day = []


                hora = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Horarios").document(doc["horario"]).get()
                hora = hora.to_dict()
                data.update({doc["horario"] : hora})
                alarm_hour = hora["hora"][0:2]
                alarm_min = hora["hora"][3:5]
                alarm_repetir = hora["repetir"]

                if(hora["repetir"] == "Diariamente"):
                    alarm_day = [1,2,3,4,5,6,7]
                elif(hora["repetir"] == "Una vez"):
                    now = datetime.now()
                    ScheduledToday = datetime(now.year,now.month,now.day,int(alarm_hour),int(alarm_min))
                    if(ScheduledToday<now):
                        alarm_day = [now.weekday() + 1]
                        print(alarm_day)
                    else:
                        alarm_day = [now.weekday()]
                        print(alarm_day)

                elif(hora["repetir"] == "Lun a Vie"):
                    alarm_day = [1,2,3,4,5]
                else:
                    for day in hora["repetir"]:
                        if(day == "Lu"):
                            alarm_day.append(0)
                        if(day == "Ma"):
                            alarm_day.append(1)
                        if(day == "Mi"):
                            alarm_day.append(2)
                        if(day == "Ju"):
                            alarm_day.append(3)
                        if(day == "Vi"):
                            alarm_day.append(4)
                        if(day == "Sa"):
                            alarm_day.append(5)
                        if(day == "Do"):
                            alarm_day.append(6)



                Dosis.append([alarm_day,alarm_hour,alarm_min,alarm_repetir,doc,pastillaid])   
                
            data.update({"dosis" : dosisdata})
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        if(len(Dosis)>0):
            ActualizarAlarmas.setAlarm(Dosis)


url = "https://firebase.google.com/?hl=es"
timeout = 10
try:
	request = requests.get(url, timeout=timeout)
	withInternet()
except (requests.ConnectionError, requests.Timeout) as exception:
    withNoInternet()


