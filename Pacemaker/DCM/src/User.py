##class that contains all user data
from src.Username import Username
from src.Password import Password
from src.Pacemaker import Pacemaker


class User:

    def __init__(self,_username,_password,_firstName,_lastName,_email):
        self.username=_username.username
        self.passwordHash=_password.passwordHash
        self.firstName=_firstName
        self.lastName=_lastName
        self.email=_email

        self.pacemaker=Pacemaker()  #create a default blank pacemaker


    

    def fstore(self):
        """return a formatted string that can store well in a text file"""
        #remember you will need to eventually search the file to find the user. 
        #maybe use json format if you want to get fancy
        return str(str(self.username)+" "+str(self.passwordHash)+" ")

    # def Save(self, upperRate, lowRate, amp, pulse)
    #     self.upper_rate = upperRate
    #     self.low_rate = lowRate
    #     self.amplitude = amp
    #     self.pulse_width = pulse