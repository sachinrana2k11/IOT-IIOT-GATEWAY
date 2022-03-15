import os
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from termcolor import colored
from CONFIGURATION.config import confi
from LOGS.logmanager import log

class AWS_IOT():
    def __init__(self):
        self.LOG = log()
        self.config = confi()
        self.certRootPath = self.config.CERTIFICATES_PATH
        try:
            self.myMQTTClient = AWSIoTMQTTClient(self.config.GATEWAY_ID)
            self.myMQTTClient.configureEndpoint(self.config.AWS_IOT_ARN, self.config.AWS_IOT_PORT)
            print(colored("SUCCESFULLY CONFIGURE TO AWS_IOT BROKER", "green"))
            self.LOG.INFO("SUCCESFULLY CONFIGURE TO AWS_IOT BROKER- " + str(os.path.basename(__file__)))
            self.load_credential()
            self.connect_server()
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR(
                "FAILED TO INIT CONFIGURE AWS_IOT BROKER" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION FAILLED TO INIT CONFIGURE AWS_IOT BROKER - " + str(e))
            pass

    def load_credential(self):
        try:
            print(colored("INIT LOAD CERTIFICATES TO AWS_IOT BROKER", "green"))
            self.LOG.INFO("INIT LOAD CERTIFICATES TO TO AWS_IOT BROKER- " + str(os.path.basename(__file__)))

            self.myMQTTClient.configureCredentials("{}root-ca.pem".format(self.certRootPath),
                                                   "{}cloud.pem.key".format(self.certRootPath),
                                                   "{}cloud.pem.crt".format(self.certRootPath))
            print(colored("SUCCESSFULLY LOAD CERTIFICATES TO AWS_IOT BROKER", "green"))
            self.LOG.INFO("SUCCESFULLY LOAD CERTIFICATES TO TO AWS_IOT BROKER- " + str(os.path.basename(__file__)))
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO LOAD AWS CERTFICATE.." + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN LOADING CERTIFICATE IN AWS IOT" + str(e))
            pass

    def connect_server(self):
        try:
            self.myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
            self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
            self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
            self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
            print(colored("CONNECTING TO AWS_IOT BROKER", "green"))
            self.LOG.INFO("CONNECTING CONFIGURE TO AWS_IOT BROKER- " + str(os.path.basename(__file__)))
            self.myMQTTClient.connect()
            print(colored("SUCCESFULLY CONNECTED TO AWS_IOT BROKER", "green"))
            self.LOG.INFO("SUCCESFULLY CONNECTED TO AWS_IOT BROKER- " + str(os.path.basename(__file__)))
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR(
                "FAILLED TO CONNECT TO THE AWS_IOT BROKER" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN CONNECTING AWS_IOT BROKER - " + str(e))
            pass

    def Aws_Iot_Send(self, payload):
        try:
            self.myMQTTClient.publish(self.config.AWS_IOT_SEND_TOPIC, payload, 0)
            print(colored("PUBLISHING  DATA TO AWS_IOT_BROKER-:" + str(payload), "green"))
            self.LOG.INFO("SUCCESFULLY SEND DATA PACKET TO AWS_IOT_BROKER" + str(os.path.basename(__file__)))
            return True
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR(
                "FAILLED TO SEND DATA TO THE AWS_IOT BROKER" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN SENDING DATA TO AWS_IOT BROKER - " + str(e))
            pass
