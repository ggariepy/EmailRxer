from threading import Thread, Lock 
from queue import Queue
import time
class TextMessenger(Thread):
    """ 
    Sends a text message to a recipient via Twilio
    """
    lock = Lock()
    
    def __init__(self, recipient, messageBody):
        Thread.__init__(self)
        self.shutdown_thread = False

        # Import the list of messages already retrieved
        self.recipient = recipient
        self.messageBody = messageBody

        # Get configs
        self.cfgfile = open("configs.json", 'rt')
        self.configs = js.load(self.cfgfile)
        self.cfgfile.close()
        self.twilioAuthToken = self.configs['twilioAuthToken']
        self.twilioAcctSID = self.configs['twilioAcctSID']
        self.twilioURI = self.configs['twilioURI']


    def run(self):
        """ 
        Makes a connection to the Twilio API 
        to send a text message
        """
        while not self.shutdown_thread:
            # Establish connection to Twilio server

            # Send message to the phone number
                       