from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore
from datetime import datetime, timedelta
import time
import json
import ActualizarAlarmas
import requests
data = {}
def withInternet():
    cred = credentials.Certificate("tt2-database-31516e0b99db.json") #descargar de https://console.cloud.google.com/iam-admin/serviceaccounts/details/101070432244239069365/keys?project=tt2-database
    #initialize_app(cred, {'storageBucket': 'tt2-database.appspot.com'})
    db = firestore.client()
    DosisIds = []
    PastillaIds = []
    ContactosIds = []
    Dosis = []
    pastillaList = {}
    contactosList = {}
    
    
    while(True):
        with open('data.json') as json_file:
            tempdata = json.load(json_file)
        data.update({"caducado" : tempdata["caducado"]})  
        time.sleep(2)
        dosisdata = []
        collection = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Dosis").get()
        pastilladata = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Pastillas").get()
        contactosdata = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Contactos").get()

        if(pastilladata != PastillaIds and str(pastilladata)=="[]"):
            PastillaIds = pastilladata
            data.update({"pastillas" : ""})  
        elif(pastilladata != PastillaIds and str(pastilladata)!="[]"):
            PastillaIds = pastilladata
            for pastilla in pastilladata:
                pastillaid = pastilla.id
                pastilla = pastilla.to_dict()
                pastillaList.update({pastillaid:pastilla})
            data.update({"pastillas" : pastillaList})  
        time.sleep(2)

        if(contactosdata != ContactosIds and str(contactosdata)=="[]"):
            ContactosIds = contactosdata
            data.update({"contactos" : ""}) 
        elif(contactosdata != ContactosIds and str(contactosdata)!="[]"):
            ContactosIds = contactosdata
            for contacto in contactosdata:
                contactoid = contacto.id
                contacto = contacto.to_dict()
                contactosList.update({contactoid:contacto})
            data.update({"contactos" : contactosList})  
        time.sleep(2)

        print(collection != DosisIds)
        print(str(collection))
        if(collection != DosisIds and str(collection)=="[]"):
            Dosis = []
            print("entró")
            DosisIds = collection
            data.update({"dosis" : ""})
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif(collection != DosisIds and str(collection)!="[]"):
            DosisIds = collection
            for doc in collection:
                docId = doc.id
                doc = doc.to_dict()
                dosisdata.append(doc)
                seguridadid = doc["seguridad"]
                if(seguridadid!= ""):
                    seguridaddata = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Seguridad").document(seguridadid).get()
                    data.update({seguridadid : seguridaddata.to_dict()})

                alarm_day = []
                if(doc["horario"]==""):
                    break
                else:
                    hora = db.collection("Users").document("2aZ3V4Ik89e9rDSzo4N9").collection("Horarios").document(doc["horario"]).get()
                hora = hora.to_dict()
                data.update({doc["horario"] : hora})
                
                alarm_hour = hora["hora"][0:2]
                alarm_min = hora["hora"][3:5]
                alarm_repetir = hora["repetir"]

                if(hora["repetir"] == "Diariamente"):
                    alarm_day = [0,1,2,3,4,5,6]
                elif(hora["repetir"] == "Una vez"):
                    now = datetime.now()
                    ScheduledToday = datetime(now.year,now.month,now.day,int(alarm_hour),int(alarm_min))
                    if(ScheduledToday<now):
                        alarm_day = [now.weekday() + 1]
                    else:
                        alarm_day = [now.weekday()]

                elif(hora["repetir"] == "Lun a Vie"):
                    alarm_day = [0,1,2,3,4]
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
                Dosis.append([alarm_day,alarm_hour,alarm_min,alarm_repetir,doc,docId])   
        
            data.update({"dosis" : dosisdata})
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        if(len(Dosis)>0):
            ActualizarAlarmas.setAlarm(Dosis)


url = "https://firebase.google.com"
timeout = 10
try:
	request = requests.get(url, timeout=timeout)
	withInternet()
except (requests.ConnectionError, requests.Timeout) as exception:
    print(exception)


