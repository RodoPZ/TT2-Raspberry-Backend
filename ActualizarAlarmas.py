import datetime
from Dispensar import Dispensar
import json
import time
def setAlarm(Dosis):
    
    alarm_days = []  
    for alarm in Dosis:
        for day in alarm[0]:
            alarm_days.append(day)
        alarm_hour = alarm[1]
        
        alarm_min = alarm[2]
        name = alarm[3]
        alarm_repetir = alarm[4]['nombre']
        dosis_Id = alarm[5]
        pills = json.loads(alarm[4]['pastillas'])
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        current_day = now.weekday()
        

        if current_day in alarm_days:
            if alarm_hour == current_hour:
                if alarm_min == current_min:
                        Dispensar(name,pills,f"{alarm_hour}:{alarm_min}",alarm_repetir,dosis_Id)
                        time.sleep(30)
