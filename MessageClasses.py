import time

class Message:
    """Defines a class which represents a single email message 
    retrieved from a POP server."""
    
    def __init__(self, _To, _From, _Date, _Subject, _Body):
       self.To = _To
       self.From = _From
       self.DateString = _Date
       self.Subject = _Subject
       self.Body = _Body 
       self.DateConv()
 
    def DateConv(self):
        # Sat, 29 Dec 2018 17:05:23 -0500
        self.TimeStamp = time.strptime(self.DateString, "%a, %d %b %Y %H:%M:%S %z") 