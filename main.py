import multiprocessing
import datetime
from datetime import *
import time

def display_update(string, linenumber):
    print(string)

def display_process():
    #display_init()
    print ("display: initialized display\n")
    line1_header = "Awesome alarm clock "
    line2_header = "Current time: "
    line3_header = "Next alarm: "
    next_alarm = "never!!!"
    while True:
        current_time = datetime.now()  # Dummy to get correct data type
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        line2 = line2_header + current_time
        line3 = line3_header + next_alarm
        display_update(line1_header, 1)
        display_update(line2, 2)
        display_update(line3, 3)
        time.sleep(1)
    print name, 'Exiting'


if __name__ == '__main__':
    display = multiprocessing.Process(target=display_process)
    display.start()