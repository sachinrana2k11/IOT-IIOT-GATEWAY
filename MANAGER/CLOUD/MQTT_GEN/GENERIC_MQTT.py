import os
import sys
import json
import paho.mqtt.client as mqtt
from termcolor import colored
from MANAGER.HANDLER.handler import *
from CONFIGURATION.config import confi
from LOGS.logmanager import log


class Generic_Mqtt():
    def __init__(self):
        self.LOG = log()
        self.config = confi()
        self.MQTT_client = mqtt.Client()
        self.LOG.INFO("MQTT CLIENT INITIALIZE - " + str(os.path.basename(__file__)))
        self.MQTT_Connect()

    def on_connect(self,client, userdata, flags, rc):
        client.subscribe(self.config.TOPIC_RECV)
        print("Subscribe topic mqtt")

    def on_message(self,client, userdata, msg):
        in_data = json.loads((msg.payload).decode("utf-8"))
        print(in_data)
        database.Save_In_DataBase()

    def MQTT_Connect(self):
        try:
            self.MQTT_client.username_pw_set(self.config.MQTT_USR, self.config.MQTT_PASS)
            self.MQTT_client.on_connect = self.on_connect
            self.MQTT_client.on_message = self.on_message
            self.MQTT_client.connect(self.config.MQTT_URL, self.config.MQTT_PORT)
            self.MQTT_client.loop_start()
            print(colored("SUCCESFULLY CONNECTED TO MQTT BROKER","green"))
            self.LOG.INFO("SUCCESFULLY CONNECTED TO MQTT BROKER- " + str(os.path.basename(__file__)))
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO CONNECT MQTT SERVER CHECK CONNECTION - " + str(os.path.basename(__file__)) + str(e))  # error logs
            print(colored("FAILLED TO CONNECT MQTT SERVER CHECK CONNECTION - " + str(e),"red"))
            pass

    def MQTT_Send_Data(self,payload):
        try:
            self.MQTT_client.publish(topic=self.config.TOPIC_SEND, payload=payload,qos=self.config.MQTT_QOS)
            print(colored("PUBLISHING  DATA TO MQTT-:" + str(payload), "green"))
            self.LOG.INFO("SUCCESFULLY SEND DATA PACKET TO MQTT BROKER" + str(os.path.basename(__file__)))
            return True
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO SEND DATA BY GENERIC MQTT" + str(os.path.basename(__file__)) + str(e))  # error logs
            print(colored("EXCEPTION IN SENDING DATA BY GENERIC MQTT - " + str(e), "red"))
            pass

