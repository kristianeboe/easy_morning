import paho.mqtt.client as mqtt
import multiprocessing
import datetime
from datetime import *
import serial
import threading
import time
from time import gmtime, strftime
import subprocess, signal
import RPi.GPIO as GPIO
import os

alarm_off_pin = 18
#ser = serial.Serial('/dev/ttyACM0',9600)
print_mutex = multiprocessing.Lock()

'''
ser = serial.Serial(
              
               port='/dev/ttyACM0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           ) 

'''

mqttc = mqtt.Client(client_id = "alarm", clean_session = True, userdata = None, protocol = "MQTTv31")

def on_connect(client, userdata, rc):
    mqttc.subscribe("bathroom/1")
    #mqttc.subscribe(userid)
    mqttc.subscribe("1")

def on_message(client, userdata, msg):
    print("received message " + str(msg.payload))
    global print_mutex
    print_mutex.acquire()
    print "on_message has mutex"
    time.sleep(1)
    #ser.write('#2')
    time.sleep(1)
    if(str(msg.payload)=="open"): 
        print "status open"
        #ser.write('status: open') # obs lcd_string(line,msg)   
    elif(str(msg.payload)=="locked"):
        print "status locked"
        #ser.write('status: locked')
    elif(str(msg.payload)=='alarm'):
        sound_alarm = multiprocessing.Process(target=alarm)
        sound_alarm.start()
    
    time.sleep(1)
    #ser.write('#1')
    time.sleep(1)
    print_mutex.release()
    print "on_message released mutex"

def display_time_process():
    global print_mutex
    while True:
        print_mutex.acquire()
        #print "clock has mutex"
        time.sleep(0.9)
        #ser.write(strftime("%a, %d %b %H:%M:%S", gmtime()))
        print_mutex.release()
        time.sleep(0.1)

def alarm():
    print "alarm started"
    global print_mutex
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(alarm_off_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #global playProcess
    myprocess = subprocess.Popen(['omxplayer', '-o' ,'alsa', 'http://stream-uk1.radioparadise.com/mp3-32'], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)    
    print_mutex.acquire()
    print "alarm has mutex"
    time.sleep(1)
    #ser.write('#3')
    time.sleep(1)
    #ser.write('Time to wake up')
    time.sleep(1)
    #ser.write('#1')
    time.sleep(1)
    print_mutex.release()
    print "alarm released mutex"
    alarm_time = 60*15 #15 minutes with radio
    while alarm_time > 0:
        if not GPIO.input(alarm_off_pin):
            break
        time.sleep(1)
        alarm_time -= 1
    
    myprocess.stdin.write('q')
    print "alarm stopped"
    print_mutex.acquire()
    print "alarm has mutex"
    time.sleep(1)
    #ser.write('#3')
    time.sleep(1)
    #ser.write('Have a good day')
    #ser.write('#1')
    time.sleep(1)
    print_mutex.release()
    print "alarm released mutex"
    myprocess.kill()
    
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'omxplayer' in line:
         pid = int(line.split(None, 1)[0])
         os.kill(pid, signal.SIGKILL)

        

def main():
    '''
    if ser.isOpen():
        ser.close()
    ser.open()
    '''
    
    display_time = multiprocessing.Process(target=display_time_process)
    display_time.start()
    
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    
    #mqttc.connect("129.241.209.166", 1883, 60)
    mqttc.connect("10.0.0.130", 1883, 60)
    mqttc.loop_forever()

if __name__ == "__main__":
    main()
