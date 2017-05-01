from datetime import datetime
import os
import json

users = os.listdir("users")


def alarm_to_datetime(alarm):
    wake_up_time = alarm["wake_up_time"]
    wake_up_days = alarm["wake_up_days"]
    print(wake_up_time)
    print(wake_up_days)


for user in users:
    file_ = open(os.path.join("users", user), "r")
    alarms = json.loads(file_.read())
    for alarm in alarms:
        alarm_to_datetime(alarm)
    # print(alarms)
