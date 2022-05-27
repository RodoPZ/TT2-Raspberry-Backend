import datetime
now = datetime.datetime.now()
def setAlarm(Dosis):
    for alarma in Dosis:
        alarm_day = alarma[0]
        alarm_hour = alarma[1]
        alarm_min = alarma[2]

        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        current_day = now.weekday()
        print(current_day)

        if alarm_day == current_day:
            print("Es el día")
            if alarm_hour == current_hour:
                print("Es la hora")
                if alarm_min == current_min:
                    print("Es el min")
