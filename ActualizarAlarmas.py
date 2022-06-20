import datetime
from Dispensar import Dispensar
import json
import time
import Caducidad
import requests
def setAlarm(Dosis):
    numstring = ""
    alarm_days = []  
    with open('data.json') as json_file:
        data = json.load(json_file)

    for pastillas in data["pastillas"]:
        date_time_obj = datetime.datetime.strptime(str(data["pastillas"][pastillas]["caducidad"]), '%d/%m/%Y')
        diference= date_time_obj.date()-datetime.datetime.now().date()
        if(diference.days<10 and data["caducado"] != str(datetime.datetime.now().date()) ):
            Caducidad.Seguridad(data["pastillas"][pastillas]["nombre"],diference.days,data["pastillas"][pastillas]["caducidad"])
            data.update({"caducado" : str(datetime.datetime.now().date())})
            for contacto in data["contactos"]:
                numstring += " " + str(data["contactos"][contacto]["numero"])
            r = requests.post('http://localhost:8080/EnviarMensajes', data=json.dumps(numstring))
            numstring = ""
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            
    for alarm in Dosis:
        for day in alarm[0]:
            alarm_days.append(day)
        alarm_hour = alarm[1]
        alarm_min = alarm[2]
        name = alarm[3]
        alarm_repetir = alarm[4]['nombre']
        dosis_Seguridad = alarm[4]['seguridad']
        dosis_contactos = []
        if(len(alarm[4]['alarmas'])>=3):
            dosis_contactos = alarm[4]['alarmas'][2:]
        for contactoDosis in dosis_contactos:
            numstring+=" " + str(data["contactos"][contactoDosis]["numero"])
        dosis_Id = alarm[5]
        pills = json.loads(alarm[4]['pastillas'])
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        current_day = now.weekday()
        print(name,pills,f"{alarm_hour}:{alarm_min}",alarm_repetir,dosis_Id,dosis_Seguridad,numstring)
        print()
        if current_day in alarm_days:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                        Dispensar(name,pills,f"{alarm_hour}:{alarm_min}",alarm_repetir,dosis_Id,dosis_Seguridad,numstring)
                        time.sleep(30)
