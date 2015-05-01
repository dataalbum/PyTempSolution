#!/usr/bin/env python

import sqlite3

import os
import time
import glob
import random

# global variables
speriod=(15*60)-1
# dbname=r'c:\sqlite\templog.db'
dname='templog.db'

# store the temperature in the database
def log_temperature(temp):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))

    # commit the changes
    conn.commit()

    conn.close()


# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print (str(row[0])+"	"+str(row[1]))

    conn.close()



# get temperature
def get_temp():

    # get temperature from usb-thermometer pcsensor executable
    output = subprocess.Popen(["/usr/local/bin/pcsensor"], stdout=subprocess.PIPE).communicate()[0]
    output2 = output.split()[4]
    temp = output2[:2]
    return temp

# main function
# This is where the program starts 
def main():

#    while True:

    # get the temperature from the device file
    temperature = get_temp()
    if temperature != None:
        print ("temperature="+str(temperature))
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature = get_temp()
        print ("temperature="+str(temperature))

        # Store the temperature in the database
    log_temperature(temperature)

        # display the contents of the database
    display_data()

#        time.sleep(speriod)

    # Uncomment to enable debug messages
if __name__=="__main__":
    main()

