import datetime

from h11 import Data
from Dispensar import Dispensar
import json


def setAlarm(Dosis):
    alarm_days = []
    for alarma in Dosis:     
        for day in alarma[0]:
            alarm_days.append(day)
        alarm_hour = alarma[1]
        alarm_min = alarma[2]
        pills = alarma[3]['pastillas']
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        current_day = now.weekday()
        

        if current_day in alarm_days:
            if alarm_hour == current_hour:
                if alarm_min == current_min:

                    Dispensar("Dosis1",pills,f"{alarm_hour}:{alarm_min}","Diario")
                    