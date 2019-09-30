from threading import Thread, Lock 
from twilio.rest import Client
import logging
import json as js
import time
class TextMessenger(Thread):
    """ 
    Sends a text message to a recipient via Twilio
    """
    lock = Lock()
    
    def __init__(self, txtMsgRecipient, txtMsgBody):
        Thread.__init__(self)
        self.shutdown_thread = False

        # Import the list of messages already retrieved
        self.txtMsgRecipient = txtMsgRecipient
        self.txtMsgBody = txtMsgBody

        # Get configs
        self.cfgfile = open("configs.json", 'rt')
        self.configs = js.load(self.cfgfile)
        self.cfgfile.close()
        self.twilioAuthToken = self.configs['twilioAuthToken']
        self.twilioAcctSID = self.configs['twilioAcctSID']
        self.twilioSourcePhone = self.configs['twilioSourcePhone']


    def run(self):
        """ 
        Makes a connection to the Twilio API 
        to send a text message
        """
        if not self.shutdown_thread:
            try:
                # Establish connection to Twilio server
                client = Client(self.twilioAcctSID, self.twilioAuthToken)

                # Send message to the phone number
                twilioMsg = client.messages.create(
                    to=self.txtMsgRecipient, 
                    from_=self.twilioSourcePhone,
                    body=self.txtMsgBody)   
            except:
                print('Connection failed!')
