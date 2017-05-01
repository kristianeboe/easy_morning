import calendar
import time
import heapq
from datetime import datetime
from threading import Timer
#TODO: import client

def epoch():
    return calendar.timegm(time.gmtime())

start_time = epoch()
heap = []
timer = None

#TODO: implement function to handle correct day
#TODO: what happens if two people set time to 0700?
def add_message(seconds, content):
    top = heap[0] if heap else None
    heapq.heappush(heap, (epoch() + seconds, content))
    if timer and top != heap[0]:
        timer.cancel()
        start()

def start():
    global timer
    if heap:
        timer = Timer(heap[0][0] - epoch(), fire)
        timer.start()

def fire():
    _, message = heapq.heappop(heap)
    
    print ('{}: {}'.format(epoch() - start_time, message))
    # call mqtt 
    start()

# get day from config file, 0 is sunday 6 
def convert_time(input_time):
	hour,min = input_time.split(':')
	second = "00"
	print(hour)
	print(min)
	now = datetime.datetime.now()
  


# add_message(seconds until user should be woken up, userid)
#convert_time("07:00",0)
add_message(5, 'message3')
start()
add_message(1, 'message4')

