#!/usr/bin/env python

#import sqlite3

import os

import mosquitto
from urllib.parse import urlparse

import psycopg2

# global variables
#dbname=r'c:\sqlite\templog.db'

# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

def insert_data(data):
    try:
        conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
    except:
        print ("I am unable to connect to the database")

# main function
# This is where the program starts 
def main():
        
    # start CloudMQTT
    mqttc = mosquitto.Mosquitto()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    #mqttc.on_log = on_log

    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://cceilikx:xeRm-2E3Wmby@m20.cloudmqtt.com:11455')
    url = urlparse(url_str)

    # Connect
    mqttc.username_pw_set(url.username, url.password)
    mqttc.connect(url.hostname, url.port)

    # Start subscribe, with QoS level 0
    mqttc.subscribe("pytemp-ins/temperature", 0)

    # Publish a message
    #mqttc.publish("pytemp-ins/temperature", message)

    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))


if __name__=="__main__":
    main()

