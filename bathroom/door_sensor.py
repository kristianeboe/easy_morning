import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

door_sensor_pin = 18

# Variables 
#MQTT_BROKER = "129.241.209.166"
MQTT_BROKER = "10.0.0.130"
MQTT_PORT = 1883 # Default port
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "bathroom/1" #TODO: hardcoded bathroom number
MQTT_USERS = (1,2,3,4)
#wake_up_time = false
#connect to broker

client = mqtt.Client(client_id = "bathroom", clean_session = True, userdata = None, protocol = "MQTTv31")

def on_connect(mosq, obj, rc):
	print "Connected to MQTT broker"
def on_publish(client, userdata, mid):
	print "Message Published..."


def door_change():
    #publish mqtt msg door locked
    time.sleep(1)
    if GPIO.input(door_sensor_pin):
        client.publish(MQTT_TOPIC, payload="locked")
        print "locked"
    else:
        print "open"
        client.publish(MQTT_TOPIC, payload="open")

def door_opened():
    #publish mqtt msg door opened
    """
    if (wake_up_time):
        wake_up_user()
    else:
        client.publish(MQTT_TOPIC, payload="open")
    """ 

def wake_up_user():
    #user = getUser() # the user we wish to wake up
    client.publish(MQTT_TOPIC, payload="alarm")   

def sensor_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(door_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(door_sensor_pin,   GPIO.BOTH,  callback=lambda x: door_change(),  bouncetime=200)
    #GPIO.add_event_detect(door_sensor_pin,   GPIO.FALLING, callback=lambda x: door_opened(),  bouncetime=200)

# Tests, remove before implementing
#door_opened()
#time.sleep(5)
#door_locked()

def main():
    # Event handlers
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    
    sensor_init()
    wake_up_user()
    while True:
        time.sleep(1)
        print "sensor: " + str(GPIO.input(door_sensor_pin))

client.disconnect()

if __name__ == "__main__":
    main()
