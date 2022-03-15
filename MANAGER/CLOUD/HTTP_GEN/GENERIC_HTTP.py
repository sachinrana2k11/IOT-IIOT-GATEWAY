import os
import sys

import requests
from termcolor import colored

from CONFIGURATION.config import confi
from LOGS.logmanager import log


class Generic_Http():
    def __init__(self):
        self.config = confi()
        self.LOG = log()
        print(colored("SUCCESFULLY INIT WITH HTTP SERVER", "green"))
        self.LOG.INFO("SUCCESFULLY INIT WITH TO HTTP SERVER- " + str(os.path.basename(__file__)))

    def HTTP_Send_data(self,payload):
        try:
            print(colored("PUBLISHING  DATA TO HTTP-:" + str(payload), "green"))
            self.LOG.INFO("SUCCESFULLY SEND DATA PACKET TO HTTP SERVER" + str(os.path.basename(__file__)))
            r = requests.post(url=self.config.HTTP_URL, data=payload)
            if self.config.HTTP_RESPONSE == "ENABLE":
                response_get = r.text
                print("The response we get :%s" % response_get)
            return True
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO SEND DATA BY GENERIC HTTP" + str(os.path.basename(__file__)) + str(e))  # error logs
            print(colored("EXCEPTION IN SENDING DATA BY GENERIC HTTP - " + str(e), "red"))
            pass