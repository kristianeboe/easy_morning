import calendar
import time
import heapq
from datetime import datetime
from threading import Timer
import door_sensor

def epoch():
    return calendar.timegm(time.gmtime())

start_time = 0
heap = []
timer = None

def add_alarm(seconds, content):
    top = heap[0] if heap else None
    #TODO: heap.heappush(heap,(start_time + diff(start_time,start_alarm), content))
    heapq.heappush(heap, (start_time + diff, content))
    if timer and top != heap[0]:
        timer.cancel()
        start()

def start():
    global timer
    if heap:
        if(heap[0][0] < start_time):
            fire()
        else:
            timer = Timer(heap[0][0] - start_time, fire)
        timer.start()

def fire():
    _, liste = heapq.heappop(heap)

    #print ('{}: {}'.format(epoch() - start_time, liste[0]))

    # if treshold > timeNow in epoch, drop.
    if (liste[2] > calendar.timegm(time.gmtime())):
        # liste[userid,start_tid,treshold]
        wake_up_user(liste)
    start()
    

def loop_dict(dict):
    global start_time
    start_time = epoch()
    # dict{"user":[[start,treshold]]}
    for key, value in dict.iteritems():
        for t in value:
            #TODO: define format of received values
            add_alarm(t[0], [key,t[0],t[1]])




