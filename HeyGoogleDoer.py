"""
HeyGoogleDoer.py
    Polls an email address seeking messages indicating actions,
    and invokes those actions for which it has a driver.

    Email messages are sent to the target email address by the
    If-This-Then-That (IFTTT) Google Assistant applet, which
    is set up in the user's IFTTT account with custom phrases
    and email messages to be sent for those phrases.
"""
from EmailRxer import EmailReceiver
from MessageClasses import Message
import queue, threading, os, sys, time, signal


def handler(signum, frame):
    global Die
    Die = True

def DoWork(message):
    print(f'Message-Id: {message.MsgId}')
    print(f'To: {message.To}')
    print(f'From: {message.From}')
    print(f'Subject: {message.Subject}')
    print(message.Body)
    print('\n---\n')

signal.signal(signal.SIGINT, handler)
Die = False
queuedmsgs = queue.Queue(5)
msglist = []
threads = []
rxworker = EmailReceiver(msglist, queuedmsgs) 
threads += [rxworker] 
rxworker.start() 
rxworker.name ='rxworker'

while len(threads) > 0:
    try:
        if Die == True:
            rxworker.shutdown_thread=True
            rxworker.join(30)
            if rxworker.is_alive == True:
                print ('rxworker thread is still alive after the join!')
            else:
                print ('rxworker thread shut down')
            quit()
        else:
            message = queuedmsgs.get(False)
            if message is not None:
                DoWork(message)
                message = None
                queuedmsgs.task_done()
    except queue.Empty:
        time.sleep(2)
        pass
        