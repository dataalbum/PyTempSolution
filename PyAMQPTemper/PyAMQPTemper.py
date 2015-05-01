#!/usr/bin/env python

import os
import json
import collections
import subprocess
import pika
import random
import time
import datetime

# global variables
speriod = 10

# get temperature
def get_temp():

    # get temperature from usb-thermometer pcsensor executable
    output = subprocess.Popen(["/usr/local/bin/pcsensor"], stdout=subprocess.PIPE).communicate()[0]
    output2 = output.split()[4]
    temperature = output2[:5]
    print (temperature)
    #temperature = random.uniform(-40, 40)

    # build json string
    # {
    #     "guid"          :   "string", <- backend takes care.
    #     "organization"  :   "string", <- no need.
    #     "displayname"   :   "string", 
    #     "location"      :   "string",
    #     "measurename"   :   "string",
    #     "unitofmeasure" :   "string",
    #     "value"         :   double/float/integer
 
    objects_list = []
    d = collections.OrderedDict()
    d['displayname'] = "TEMPer1F_V1.3"
    d['location'] = "Inside"
    d['measurename'] = "Temperature"
    d['unitofmeasure'] = "C"
    d['value'] = temperature
    d['timestamp'] = str(datetime.datetime.now())
    objects_list.append(d)
    
    json_string = json.dumps(objects_list)
    
    return json_string

def send_temp(message):
    # Parse CLODUAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://ontpcbos:7G7Ilh2wbERfJNHZMhfHTHJPaj4GDGu1@bunny.cloudamqp.com/ontpcbos')
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    
    #channel.queue_declare(queue='temperature') # Declare a queue
    channel.exchange_declare(exchange='temperature',
                             type='fanout') # Declare a topic
    # send a message
    channel.basic_publish(exchange='temperature', routing_key='', body=message)
    print (" [x] Sent: " + message)

    connection.close()

# main function
# This is where the program starts 
def main():
    
    #while True:

        # get temp
        temp=get_temp()

        #send temp
        send_temp(temp)
    
        #time.sleep(speriod)

if __name__=="__main__":
    main()
