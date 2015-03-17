import unirest
import json
import paho.mqtt.client as mqtt
import sys
import configparser
import os

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('/home/pi/peoplecounter/counter.ini')

username = settings.get('MQTT', 'username')
password = settings.get('MQTT', 'password')
mqtthost = settings.get('MQTT', 'mqtthost')
countertopic = settings.get('MQTT', 'countertopic')
peopletopic  = settings.get('MQTT', 'peopletopic')
api_key = settings.get('PHOTO_KEYS', 'api_key')
api_secret = settings.get('PHOTO_KEYS', 'api_secret')
mashape_key = settings.get('PHOTO_KEYS', 'mashape_key')
photo = str(sys.argv[1])

response = unirest.post("https://face.p.mashape.com/faces/detect?api_key=" + api_key + "&api_secret=" + api_secret,
  headers={
    "X-Mashape-Key": mashape_key,
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
  },
  params={
    "attributes": "all",
    "detector": "Aggressive",
    "files": open(photo, mode="r") 
  }
)

os.remove(photo)

client = mqtt.Client()
client.username_pw_set(str(username), str(password))
client.connect(str(mqtthost))

photo = json.loads(response.raw_body)

client.publish(str(peopletopic), response.raw_body);
