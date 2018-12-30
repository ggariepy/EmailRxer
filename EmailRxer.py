#!/usr/bin/env python3
#  EmailRxer.py
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

M = pop.POP3(popServer)
M.user(popUser)
M.pass_(popPass)
messageBody = False
Messages = {}
headers = {}
Body = ''
numMessages = len(M.list()[1])
for messagenum in range(numMessages):
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
    #M.dele(messagenum + 1)        
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

print ("Enqueued " + str(msgQueue._qsize()) + " messages")