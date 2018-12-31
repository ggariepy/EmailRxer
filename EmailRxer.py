#!/usr/bin/env python3
#  EmailRxer.py
""" Polls the email account configured in configs.json
    and retrieves new messages, decodes them into their
    component parts, converts them to instances of the
    Message class, and places them into a FIFO queue.
    Typically deletes messages after retrieving them;
    this behavior can be changed by configuring the
    deleteMsgs item in configs.json to false.   
"""
import poplib as pop
import json as js
import MessageClasses as mclass
import queue

# Get configs
file = open("configs.json", 'rt')
configs = js.load(file)
file.close()
popUser = configs['popUser']
popPass = configs['popPass']
popServer = configs['popServer']
popPort = configs['popPort']
pollFreq = configs['pollFreq']
deleteMsgs = configs['deleteMsgs']

# Establish connection to POP3 server
M = pop.POP3(popServer)
M.user(popUser)
M.pass_(popPass)

# If there are messages, decode them from 
# byte arrays and retrieve the headers we
# want and their message bodies
Messages = {}
numMessages = len(M.list()[1])
for messagenum in range(numMessages):
    headers = {}
    Body = ''
    messageBody = False
    for line in M.retr(messagenum+1)[1]:
        if messageBody == False:
            segments = line.split(b': ')
            if len(segments) > 1:
                key = segments[0].decode('ASCII')
                val = segments[1].decode('ASCII')
                if key == 'Content-Type':
                    messageBody = True
                    headers[key] = val
                elif key == 'From' or key == 'Message-ID' \
                or key == 'Date' or key == 'Subject' \
                or key == 'To':
                    headers[key] = val
        else: Body += line.decode('ASCII')
    Messages[messagenum] = (headers, Body)
    deleteMsgs and M.dele(messagenum + 1)        
M.quit()

print ("Retrieved " + str(numMessages) + " message(s).")

msgQueue = queue.Queue(0)
for msg in Messages.items():
    headers = msg[1][0]
    strBody = msg[1][1]
    strTo = headers["To"]
    strFrom = headers["From"]
    strSubject = headers["Subject"]
    strDate = headers["Date"]
    thismsg = mclass.Message(strTo, strFrom, strDate, strSubject, strBody)
    msgQueue.put(thismsg)

print ("Enqueued " + str(msgQueue._qsize()) + " message(s)")