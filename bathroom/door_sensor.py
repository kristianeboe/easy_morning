import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from datetime import datetime, time
import time
import multiprocessing
from multiprocessing import Value, Array
import calendar

door_sensor_pin = 18
#door_status = False

# Variables 
MQTT_BROKER = "129.241.209.166"
#MQTT_BROKER = "10.0.0.130"
MQTT_PORT = 1883 # Default port
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_USERS = (1,2,3,4)
#wake_up_time = false
#connect to broker


TOPIC_ALARM = "alarm/"
TOPIC_NEW_UNIT = "new/alarm/unit"
TOPIC_STATUS = "bathroom/status"
TOPIC_CONFIG_INITIAL = "config/initial"
TOPIC_CONFIG = "config/"

userid = '007'

client = mqtt.Client(client_id = "bathroom", clean_session = True, userdata = None, protocol = "MQTTv31")

def on_connect(mosq, obj, rc):
    print "Connected to MQTT broker"
    client.subscribe("new/alarm/unit")
    #door_change()
def on_publish(client, userdata, mid):
    print "Message Published..."

def on_message(client, userdata, msg):
    print "Received some message: " + str(msg.payload)
    if msg.topic == TOPIC_NEW_UNIT:
        # some function id=create_new_user_id()
        client.publish("config/initial", payload = userid)
        print "Halla, new alarm unit is added"
    

def door_change(door):
    #publish mqtt msg door locked
    #global door_status
    time.sleep(1)
    if GPIO.input(door_sensor_pin):
        print "New status: open"
        door.value = True
        client.publish(TOPIC_STATUS, payload="open")
    else:
        print "New status: locked"
        door.value = False
        client.publish(TOPIC_STATUS, payload="locked")


def wake_up_user(user):
    while user.start <= calendar.timegm(time.gmtime()) < user.start + user.threshold:
        if door_status:
            time.sleep(10)
            client.publish(TOPIC_ALARM + userid, payload="Wake up!")
            time.sleep(180) # 3 min to move his lazy ass to the toilet
            break
        time.sleep(5)    

def wake_up_user_testing(door):
    #userid = getUser() # the user we wish to wake up
    
    global alarm_time
    #global door_status
    threshold = 10000
    alarm_time = 1705
    now_time = 1703
    while now_time < alarm_time:
        print "TESTING: Waiting for time to be enough"
        now_time += 1
        time.sleep(5)

    while alarm_time <= now_time < alarm_time + threshold:
        print "TESTING: Waiting for door to open"
        if door.value == True:
            client.publish(TOPIC_ALARM + userid, payload="Wake up!")
            print "TESTING: Published wake up message to userid: " + userid
            time.sleep(5)
            break

        time.sleep(1)
        now_time += 1


def sensor_init(door):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(door_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(door_sensor_pin,   GPIO.BOTH,  callback=lambda x: door_change(door),  bouncetime=2000)
    #GPIO.add_event_detect(door_sensor_pin,   GPIO.FALLING, callback=lambda x: door_opened(),  bouncetime=200)

# Tests, remove before implementing
#door_opened()
#time.sleep(5)
#door_locked()

def print_door_status(door):
    while True:
        time.sleep(1)
        sensor_status = str(GPIO.input(door_sensor_pin))
        print ("Sensor status: {}, Door status variable: {}".format(sensor_status, door.value))


def main():
    door_status = Value('i', 0)
    sensor_init(door_status)
    
    # Event handlers
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    
    wake_up = multiprocessing.Process(target=wake_up_user_testing, args=(door_status,))
    door_status_thread = multiprocessing.Process(target=print_door_status, args=(door_status,))
    
    wake_up.start()
    door_status_thread.start()
    door_change(door_status)
    client.loop_forever()


    #wake_up_user()
   

client.disconnect()

if __name__ == "__main__":
    main()
