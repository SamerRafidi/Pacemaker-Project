import hashlib


from src.Utils import special_characters

class invalidUsername(Exception):

    def __init__(self, message="Invalid Password"):
        self.message=message
        super().__init__(self.message)


class Password:
    
    def __init__(self,_password):
        if(self.validatePassword(_password)==False):
            print("Password invalid\n")

        else:
            self.passwordHash=self.getPasswordHash(_password)

    def validatePassword(self,_password):
        """check documentation on what a password must contain"""
        return (self.validateLength(_password) and
                self.validateSpecial(_password) and
                self.validateCaps(_password) )

    def validateLength(self,_password):
        return True
        pass
 

    def validateSpecial(self,_password):
        return True
        pass


    def validateCaps(self,_password):
        return True
        pass

    def getPasswordHash(self,_password):
        """get the sha256 representation of the password. look into hashlib library for this"""
        #return hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
        return hashlib.sha224(bytes(_password,'ascii')).hexdigest()



    