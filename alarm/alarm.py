import datetime
import threading
import sys

def ring_ring():
	# call alarm function to sound alarm
	sys.stdout.write("ring ring\n")
	sys.stdout.flush()

Class Clock: 
	
	def __init__(self):
		self.alarm_time = None
		self._alarm_thread = None
		self.update_interval = 1
		self.event = threading.Event()
		self.already_woken_up = False

	def run(self):
		while True:
			self.event.wait(self.update_interval)
			if self.event.isSet():
				break
			now = datetime.datetime.now()
			if self._alarm_thread and self._alarm_thread.is_alive():
				alarm_symbol = "+"
			else:
				alarm_symbol = " "
			sys.stdout.write(("\r%02d:%02d:%02d %s") % (now.hour, now.minute, now.second, alarm_symbol))
			sys.stdout.flush()

	def set_alarm(self,hour,minute):
		now = datetime.datetime.now()
		alarm = now.replace(hour=int(hour), minute=int(minute))
		delta = int((alarm - now).total_seconds())
		if delta <= 0 or already_woken_up:
			self._alarm_thread.cancel()
		self._alarm_thread = threading.Timer(delta, ring_ring)
		self._alarm_thread.daemon = True
		self._alarm_thread.start()

clock = Clock()
# clock.set_alarm(user.end.hour, user.end.minute)
# https://stackoverflow.com/questions/16578652/threading-timer
clock.set_alarm(sys.argv[1], sys.argv[2])
clock.run
