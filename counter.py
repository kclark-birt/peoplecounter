import RPi.GPIO as GPIO
import time
import subprocess
import paho.mqtt.client as mqtt
import os
import configparser
import time
import sys

print "Reading configuration file........",

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('/home/pi/peoplecounter/counter.ini')

username = settings.get('MQTT', 'username')
password = settings.get('MQTT', 'password')
mqtthost = settings.get('MQTT', 'mqtthost')
countertopic = settings.get('MQTT', 'countertopic')
peopletopic  = settings.get('MQTT', 'peopletopic')

projectroot  = settings.get('PEOPLECOUNTER', 'projectroot')
photocache   = projectroot + "photocache/"

print "[DONE]"

print "Setting up GPIO pins..............",

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

print "[DONE]"

print "Setting up MQTT Client............",

client = mqtt.Client()
client.username_pw_set(str(username), str(password))
client.connect(str(mqtthost))

print "[DONE]"

counter = 0
peoplev = 0
peoplecount = 0
print "========================================="
print "Configuration completed, counting people!"
print "========================================="
while(1):
   sys.stdout.flush()
   print "\rCurrent count: " + str(peoplecount), 
   
   presence = GPIO.input(21)
   if(presence):
      peoplecount += 1
      timestamp = int(time.time())
      payload = "{\"timestamp\": " + str(timestamp) + ", \"counter\": " + str(peoplecount) +"}" 
      file = photocache + str(peoplecount) + ".png"
      cmd1 = "raspistill -w 400 -h 300 -vf -e png -q 100 -o " + photocache + str(peoplecount) + ".png"
      cmd2 = "python " + projectroot + "detect.py " + file 
      client.publish("counter", str(payload));
      #pid1 = subprocess.call(cmd1, shell=True)
      #os.system("python " + projectroot + "detect.py " + file)
      #subprocess.Popen("python " + projectroot + "detect.py " + file, shell=True)
      presence = 0
      time.sleep(1.5)
   time.sleep(1)
   counter += 1
   if(counter==10):
      counter = 0
      peoplev = 0
