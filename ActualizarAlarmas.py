import datetime
from Dispensar import Dispensar
import json
import time
def setAlarm(Dosis):
    
    alarm_days = []  
    for day in Dosis[0]:
        alarm_days.append(day)

    alarm_hour = Dosis[1]
    alarm_min = Dosis[2]
    name = Dosis[3]
    alarm_repetir = Dosis[4]['nombre']
    dosis_Id = Dosis[5]
    pills = json.loads(Dosis[4]['pastillas'])
    now = datetime.datetime.now()
    current_hour = now.strftime("%H")
    current_min = now.strftime("%M")
    current_day = now.weekday()
    

    if current_day in alarm_days:
        if alarm_hour == current_hour:
            if alarm_min == current_min:
                    Dispensar(name,pills,f"{alarm_hour}:{alarm_min}",alarm_repetir,dosis_Id)
                    time.sleep(30)
