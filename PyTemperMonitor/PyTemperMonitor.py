#!/usr/bin/env python

import os
import json
import collections
import subprocess
import pika
import random
import time
import datetime
import requests
from requests.exceptions import ConnectionError

# global variables
speriod = 10
measure_name = "Temperature"

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
    d['measurename'] = measure_name
    d['unitofmeasure'] = "C"
    d['value'] = temperature
    d['timestamp'] = str(datetime.datetime.now())
    d['year'] = str(datetime.datetime.today().year)
    d['month'] = str(datetime.datetime.today().month)
    d['day'] = str(datetime.datetime.today().day)
    objects_list.append(d)
    
    json_string = json.dumps(objects_list)
    
    return json_string

def send_temp(message):
    print message
    uri     = "http://127.0.0.1:3000/log"
    headers = {'Content-Type' : 'application/json'}
    try:
        res = requests.post(uri, message, headers=headers)
        print res.json
    except ConnectionError as e:
        print e
        res = "No response"
    
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
