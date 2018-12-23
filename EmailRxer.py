#!/usr/bin/env python3
#  EmailRxer.py
import poplib as pop
import json as js

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
                key = str(segments[0])
                val = str(segments[1])
                if key == 'Content-Type':
                    messageBody = True
                    headers[key] = val
                elif key == 'From' or key == 'Message-ID' \
                or key == 'Date' or key == 'Subject' \
                or key == 'To':
                    headers[key] = val
        else: Body += line
    Messages[messagenum] = (headers, Body)
    M.dele(messagenum + 1)        
M.quit()

print ("Retrieved " + str(numMessages) + " message(s).")

for msg in Messages:
    headers = msg[0]
    body = msg[1]
    print("To: " + headers["To"])
    print ("From: " + headers["From"])
    print ("Subject: " + headers["Subject"])
    print ("Date:"  + headers["Date"])
    print ("Body:\n" + body)
    print ("\n----\n")
