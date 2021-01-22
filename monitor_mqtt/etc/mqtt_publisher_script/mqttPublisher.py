#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import csv
import json

# client, user and device details
serverUrl   = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
clientId    = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
tenant      = "xxxxxx"
username    = "xxxxxxxxxxxxxxxxxxx"
password    = "xxxxxxxxxxxxxxxxxx"

receivedMessages = []
csvFilePath = r'samplecsvfile.csv'

def callFile():
    List=[]
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            List.append(rows)
        return List

def start():
    List = callFile()
    msg = {}
    try:
       for row in List:
           msg['d']=row
           json_msg = json.dumps(msg, indent=4)
           sendMeasurements(json_msg)
           time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("Received keyboard interrupt, quitting ...")
    finally:SystemExit


# send temperature measurement
def sendMeasurements(msg):
    try:
        publish("iot-2/type/iotsensor-demo/id/simulatordevice/evt/iotsensor/fmt/json",msg )
        print("Message published {}".format(msg))
    except (KeyboardInterrupt, SystemExit):
        print("Received keyboard interrupt, quitting ...")

# publish a message
def publish(topic, message, waitForAck = False):
    mid = client.publish(topic, message, 2)[1]
    if (waitForAck):
        while mid not in receivedMessages:
            time.sleep(0.25)

def on_publish(client, userdata, mid):
    receivedMessages.append(mid)

# connect the client to Cumulocity IoT and register a device
client = mqtt.Client(clientId)
client.username_pw_set(username, password)
client.on_publish = on_publish

client.connect(tenant+'.'+serverUrl)
client.loop_start()
print("Device registered successfully!")
start()
