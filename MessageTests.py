from MessageClasses import Message
from unittest import TestCase, main as unittest_main

class TestMsg(TestCase):
    """
    Test the creation of a Message object from the MessageClasses library
    """
 
    def setUp(self):
        """ Set up a test instance of the Message class""" 
        self.testMsg = Message(
            To='geoff.gariepy@gmail.com',
            From='somebody@somewhere.com',
            DateString='Mon, 31 Dec 2018 23:59:59 -0500',
            Subject='Hello, world',
            Body='Hi there, Geoff'
        )

    def tearDown(self):
        del self.testMsg

    def test_To(self):
        self.assertEqual(self.testMsg.To, 'geoff.gariepy@gmail.com', msg='To test failed')
    
    def test_From(self):
        self.assertEqual(self.testMsg.From, 'somebody@somewhere.com', msg='From test failed')
    
    def test_DateString(self):
        self.assertEqual(self.testMsg.DateString, 'Mon, 31 Dec 2018 23:59:59 -0500', msg='DateString test failed')
    
    def test_Subject(self):
        self.assertEqual(self.testMsg.Subject, 'Hello, world', msg='Subject test failed')

    def test_Body(self):
        self.assertEqual(self.testMsg.Body, 'Hi there, Geoff', msg='Body test failed')

    def test_time_month(self):
        self.assertEqual(self.testMsg.TimeStamp.tm_mon, 12, msg='TimeStamp month test failed')

if __name__ == '__main__':
    unittest_main()