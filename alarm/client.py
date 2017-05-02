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

userid = "blahblah"
alarm_off_pin = 18
#ser = serial.Serial('/dev/ttyACM0',9600)
print_mutex = multiprocessing.Lock()




ser = serial.Serial(
              
               port='/dev/ttyACM0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           ) 





# Variables 
MQTT_BROKER = "129.241.209.166"
#MQTT_BROKER = "10.0.0.130"
MQTT_PORT = 1883 # Default port
MQTT_KEEPALIVE_INTERVAL = 45

TOPIC_ALARM = "alarm/"
TOPIC_NEW_UNIT = "new/alarm/unit"
TOPIC_STATUS = "bathroom/status"
TOPIC_CONFIG_INITIAL = "config/initial"
TOPIC_CONFIG = "config/"


client = mqtt.Client(client_id = "alarm", clean_session = True, userdata = None, protocol = "MQTTv31")




def on_connect(client, userdata, rc):
    global userid
    print "Connected to MQTT broker"
    if os.path.exists('/home/pi/easy_morning/alarm/config.txt'):
        file = open("config.txt","r")
        userid = file.readline()
        file.close()
        print "userid: " + userid
        client.subscribe(TOPIC_CONFIG + userid)
        client.subscribe(TOPIC_STATUS)
        client.subscribe(TOPIC_ALARM + userid)
    else:
        client.subscribe(TOPIC_CONFIG_INITIAL)
        #client.subscribe(userid)
        client.subscribe(TOPIC_STATUS)
        client.publish(TOPIC_NEW_UNIT, payload="I need a toilet! Ho ho ho")
        print "Published on topic new/alarm/unit"

def on_publish(client, userdata, mid):
    print "Message Published..."

def on_message(client, userdata, msg):
    global userid
    print("received message on topic: " + msg.topic + ", "+ str(msg.payload))
    if msg.topic == TOPIC_CONFIG_INITIAL:
        print "Should have received some config"
        file = open("config.txt","w+")
        file.write(str(msg.payload))
        file.close()
        userid = str(msg.payload)
        print "userid: " + userid


    elif msg.topic == TOPIC_STATUS:    
        global print_mutex
        print_mutex.acquire()
        print "on_message has mutex"
        time.sleep(1)
        ser.write('#2')
        time.sleep(1)
        if(str(msg.payload)=="open"): 
            print "status open"
            ser.write('status: open') # obs lcd_string(line,msg)   
        elif(str(msg.payload)=="locked"):
            print "status locked"
            ser.write('status: locked')
        time.sleep(1)
        ser.write('#1')
        time.sleep(1)
        print_mutex.release()
        print "on_message released mutex"

    elif msg.topic == TOPIC_ALARM + userid:
        sound_alarm = multiprocessing.Process(target=alarm)
        sound_alarm.start()
        
def display_time_process():
    global print_mutex
    while True:
        print_mutex.acquire()
        #print "clock has mutex"
        time.sleep(0.9)
        ser.write(strftime("%a, %d %b %H:%M:%S", gmtime()))
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
    ser.write('#3')
    time.sleep(1)
    ser.write('Time to wake up')
    time.sleep(1)
    ser.write('#1')
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
    ser.write('#3')
    time.sleep(1)
    ser.write('Have a good day')
    ser.write('#1')
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
    global userid

    '''
    if ser.isOpen():
        ser.close()
    ser.open()
    '''
    
    display_time = multiprocessing.Process(target=display_time_process)
    display_time.start()
  
    # Event handlers
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    client.loop_forever()
    
   
    '''
    if os.path.exists('/home/pi/easy_morning/alarm/config.txt'):
        file = open("config.txt", "r")
        userid = file.readline()
        print ("User ID: {}".format(file.readline()))

    else:   
        client.publish("new_alarm_unit", payload="I need a toilet! Ho ho ho")
        print "Published on topic new_alarm_unit"
    '''   
    



if __name__ == "__main__":
    main()
