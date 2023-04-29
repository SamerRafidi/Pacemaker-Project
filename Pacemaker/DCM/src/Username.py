from src.Utils import special_characters

class invalidUsername(Exception):

    def __init__(self, message="Invalid Username"):
        self.message=message
        super().__init__(self.message)


class Username:

    def __init__(self,_username):
        self.username = _username
        # if(self.performValidation(_username)==False):
        #     print("User not created\n")
        # else:
        #     self.username = _username


    def performValidation(self,_username):
        """check if the username is valid"""
        if(_username[0].isnumeric()==True):
            return False
        elif(any(c in special_characters for c in _username[0])):
            return False
        elif(' ' in _username):
            return False

        return True


