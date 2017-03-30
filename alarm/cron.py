import collections
from crontab import CronTab

cron = CronTab(user=True)




msg = collections.namedtuple('msg', 'minute, hour, day')

msg.minute = 44
msg.hour   = 9
msg.day    = 'THU'


cmd = 'python /home/haagon/GIT/easy_morning/alarm/alarm.py'
job = cron.new(command=cmd)




job.minute.on(msg.minute)
job.hour.on(msg.hour)
job.dow.on(msg.day)


cron.write()
