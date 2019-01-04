import time
from dataclasses import dataclass, field

@dataclass(order=True)
class Message:
    """
    This class represents a single email message 
    retrieved from a POP server.  
    Fields:
    MsgId <str> (The hopefully unique ID for this message)
    To <str>    (To: string from the message headers)
    From <str>  (From: string from the message headers)
    DateString <str>, e.g. Fri, 31 Dec 1999 23:59:59 -0500
    Subject     (Subject: string from the message headers)
    Body        (The complete message body represented as ASCII)
    """
    MsgId: str
    To: str
    From: str
    Date: str
    Subject: str
    Body: str

    def __post_init__(self):
        """ 
        Creates the TimeStamp attribute by
        converting the text DateString to a time value
        """
        self.TimeStamp = time.strptime(self.Date, "%a, %d %b %Y %H:%M:%S %z") 
