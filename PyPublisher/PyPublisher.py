#!/usr/bin/env python

import sqlite3

import os

import mosquitto
from urllib.parse import urlparse

import json
import collections

# global variables
dbname=r'c:\sqlite\templog.db'

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

# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    
    curs.execute("SELECT timestamp, temp FROM temps")
    
    # Convert query to objects of key-value pairs
    rows = curs.fetchall()

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['timestamp'] = row[0]
        d['temp'] = row[1]
        objects_list.append(d)
 
    json_string = json.dumps(objects_list)

    #json_string = json.dumps(dict(curs.fetchall()))
    #data = str(curs.fetchall())
    #print (json_string)
#    for row in curs.execute("SELECT * FROM temps"):
#            timestamp = row[0]
#            temp = row[1]
#            print (str(timestamp) + "|" + str(temp))
    
    conn.close()

    return json_string

# main function
# This is where the program starts 
def main():
    
    # display the contents of the database
    message = display_data()
    print ("Message: " + message)
    
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
    #mqttc.subscribe("pytemp-ins/temperature", 0)

    # Publish a message
    mqttc.publish("pytemp-ins/temperature", message)

    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))


if __name__=="__main__":
    main()
