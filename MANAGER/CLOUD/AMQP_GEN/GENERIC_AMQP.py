import os
import sys

import pika
from termcolor import colored

from CONFIGURATION.config import confi
from LOGS.logmanager import log


class Generic_Amqp():
    def __init__(self):
        try:
            self.LOG = log()
            self.config = confi()
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config.AMQP_URL))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.config.AMQP_QUEUE)
            self.LOG.INFO("AMQP CLIENT INITIALIZE - " + str(os.path.basename(__file__)))
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO INIT GENERIC AMQP" + str(os.path.basename(__file__)) + str(e))  # error logs
            print(colored("EXCEPTION IN INIT GENERIC AMQP - " + str(e), "red"))
            pass

    def AMQP_Send_data(self,payload):
        try:
            self.channel.basic_publish(exchange=self.config.AMQP_EXCHANGE, routing_key=self.config.AMQP_ROUTING_KEY, body=payload)
            print(colored("PUBLISHING  DATA TO AMQP-:" + str(payload), "green"))
            self.LOG.INFO("SUCCESFULLY SEND DATA PACKET TO AMQP BROKER" + str(os.path.basename(__file__)))
            return True
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO SEND DATA BY GENERIC AMQP" + str(os.path.basename(__file__)) + str(e))  # error logs
            print(colored("EXCEPTION IN SENDING DATA BY GENERIC AMQP - " + str(e), "red"))
            pass






