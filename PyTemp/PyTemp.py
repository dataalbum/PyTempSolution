#!/usr/bin/env python

import sqlite3

import os
import time
import glob
import random

# global variables
speriod=(15*60)-1
dbname=r'c:\sqlite\templog.db'



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



# get temerature
# returns None on error, or the temperature as a float
def get_temp():

    # get the status from the end of line 1 
    status = "YES"

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        print (status)
        tempvalue=random.uniform(-40, 40)
        print (tempvalue)
        return tempvalue
    else:
        print ("There was an error.")
        return None


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

