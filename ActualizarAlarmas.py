import datetime
from Dispensar import Dispensar
import json

def setAlarm(Dosis):
    
    alarm_days = []
    for alarma in Dosis:   #cambiar para solo una hora 
        for day in alarma[0]:
            alarm_days.append(day)

        alarm_hour = alarma[1]
        alarm_min = alarma[2]
        name = alarma[3]
        alarm_repetir = alarma[4]['nombre']
        pills = json.loads(alarma[4]['pastillas'])
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        current_day = now.weekday()
        

        if current_day in alarm_days:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                    Dispensar(name,pills,f"{alarm_hour}:{alarm_min}",alarm_repetir)
                    
