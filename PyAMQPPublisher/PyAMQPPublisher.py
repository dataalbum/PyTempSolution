#!/usr/bin/env python

import sqlite3

import os

import urlparse

import json
import collections

import pika
import logging
logging.basicConfig()

# global variables
dbname=r'c:\sqlite\templog.db'

# CloudAMQP
# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print (" [x] Received %r" % (body))

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
    #print ("Message: " + message)
    
    # Parse CLODUAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://ontpcbos:7G7Ilh2wbERfJNHZMhfHTHJPaj4GDGu1@bunny.cloudamqp.com/ontpcbos')
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='temperature') # Declare a queue
    # send a message
    channel.basic_publish(exchange='', routing_key='temperature', body=message)
    print (" [x] Sent: " + message)

    connection.close()

if __name__=="__main__":
    main()
