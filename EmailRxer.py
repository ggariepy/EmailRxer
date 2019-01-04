from threading import Thread, Lock 
import poplib as pop
import json as js
from MessageClasses import Message
from queue import Queue
import time
class EmailReceiver(Thread):
    """ 
    Polls the email account configured in configs.json
    and retrieves new messages, decodes them into their
    component parts, converts them to instances of the
    Message class, and places them into a FIFO queue.
    Typically deletes messages after retrieving them;
    this behavior can be changed by configuring the
    deleteMsgs item in configs.json to false.   
    """
    lock = Lock()
    
    def __init__(self, MessageList, MessageQueue):
        Thread.__init__(self)
        self.shutdown_thread = False

        # Import the list of messages already retrieved
        self.AlreadyRead = []
        for msg in MessageList:
            self.AlreadyRead.append(msg.MsgId)

        # Get configs
        self.cfgfile = open("configs.json", 'rt')
        self.configs = js.load(self.cfgfile)
        self.cfgfile.close()
        self.popUser = self.configs['popUser']
        self.popPass = self.configs['popPass']
        self.popServer = self.configs['popServer']
        self.popPort = self.configs['popPort']
        self.pollFreq = self.configs['pollFreq']
        self.deleteMsgs = self.configs['deleteMsgs']
        self.MsgQueue = MessageQueue


    def run(self):
        """ 
        Polls the POP3 server and creates instances of
        the Message class for any email not seen until
        now.
        """
        while not self.shutdown_thread:
            # Establish connection to POP3 server
            self.PopSrvConn = pop.POP3(self.popServer)
            self.PopSrvConn.user(self.popUser)
            self.PopSrvConn.pass_(self.popPass)
            newMsgs = 0
            numMessages = len(self.PopSrvConn.list()[1])
            # If there are messages, decode them from 
            # byte arrays and retrieve the headers we
            # want and the message bodies
            for messagenum in range(numMessages):
                headers = {}
                Body = ''
                messageBody = False
                for line in self.PopSrvConn.retr(messagenum+1)[1]:
                    if messageBody == False:
                        segments = line.split(b': ')
                        if len(segments) > 1:
                            key = segments[0].decode('ASCII')
                            val = segments[1].decode('ASCII') or ''
                            if key == 'Content-Type':
                                messageBody = True
                                headers[key] = val
                            elif key == 'From' or key == 'Message-ID' \
                            or key == 'Date' or key == 'Subject' \
                            or key == 'To':
                                headers[key] = val
                    else: Body += line.decode('ASCII')
                if self.AlreadyRead.count(headers['Message-ID']) == 0:
                    # Haven't seen this message before, so create an
                    # instance of the Message class from it.
                    newMsgs += 1
                    strMsgId = headers['Message-ID']
                    strTo = headers['To']
                    strFrom = headers['From']
                    strSubject = headers['Subject']
                    strDate = headers['Date']
                    thismsg = Message(strMsgId, strTo, strFrom, strDate, strSubject, Body)
                    EmailReceiver.lock.acquire()
                    self.MsgQueue.put(thismsg)
                    self.AlreadyRead.append(strMsgId)
                    EmailReceiver.lock.release()
                self.deleteMsgs and self.PopSrvConn.dele(messagenum + 1)        
            self.PopSrvConn.quit()
            self.RetrieveStatus = f'Retrieved {str(newMsgs)} message(s).' 
            time.sleep(self.pollFreq)
        print("EmailReceiver worker thread shutting down.")