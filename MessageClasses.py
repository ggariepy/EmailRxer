import time
from dataclasses import dataclass, field

@dataclass(order=True)
class Message:
    """
    Defines a class which represents a single email message 
    retrieved from a POP server.  
    Fields:
    To <str>
    From <str> 
    DateString <str>, e.g. Fri, 31 Dec 1999 23:59:59 -0500
    Subject 
    Body
    """
    To: str
    From: str
    Subject: str
    Body: str
    DateString: str = field(default='Fri, 31 Dec 1999 23:59:59 -0500')

    def __post_init__(self):
        """ 
        Creates the TimeStamp attribute by
        converting the text DateString to a time value
        """
        self.TimeStamp = time.strptime(self.DateString, "%a, %d %b %Y %H:%M:%S %z") 
