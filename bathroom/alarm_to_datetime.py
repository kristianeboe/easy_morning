from datetime import datetime, time, timedelta
import os
import json

users = os.listdir("users")


def format_time(time):
    if ":" in time:
        return time[0:2] + time[3:]
    else:
        return time

def alarms_to_datetime(alarm):
    wake_up_time = alarm["wake_up_time"]
    wake_up_days = format_time(alarm["wake_up_days"])
    wake_up_hour = int(wake_up_time[0:2])
    wake_up_minute = int(wake_up_time[3:4])


    now = datetime.now().weekday()+1 if datetime.now().weekday() < 6 else 0

    alarms = []

    print(wake_up_hour, wake_up_minute)
    for wake_up_day in wake_up_days:
        delta = int(wake_up_day) - now
        alarm_ = datetime.now()

        if delta < 0:
            delta = delta + 7

        if delta == 0:
            if datetime.now() > datetime.now().replace(hour=wake_up_hour, minute=wake_up_minute):
                alarm_ = datetime.now() + timedelta(days=7)
        else:
            alarm_ = datetime.now() + timedelta(days=delta)
        
        alarm_ = alarm_.replace(hour=wake_up_hour, minute=wake_up_minute, second=0, microsecond=0)
        alarms.append(alarm_)
    
    return alarms

        # print("delta", delta)

        # new_datetime = timedelta()

        # print(new_datetime)
    # print(now)


user_to_alarm_datetime = {}
for user in users:
    # print(user)
    file_ = open(os.path.join("users", user), "r")
    alarms = json.loads(file_.read())
    user_to_alarm_datetime[user] = []
    for alarm in alarms:
        alarms_datetime = alarms_to_datetime(alarm)
        user_to_alarm_datetime[user].append([alarm_datetime.isoformat() for alarm_datetime in alarms_datetime])


lol = json.dumps(user_to_alarm_datetime)
print(lol)
    # print(alarms)
