Class user(oject):
	user_id = ""
	alarms = []
	def __init__(self, user_id, alarms):
		self.user_id = user_id
		self.alarms = alarms

Class alarms(object):
	alarm_id = ""
	wake_up_time = 0
	buffer = 0
	days = []
	on = false
	def __init__(self, alarm_id, wake_up_time, buffer, days, on):
		self.alarm_id = ""
	        self.wake_up_time = 0
        	self.buffer = 0
        	self.days = []
        	self.on = false

