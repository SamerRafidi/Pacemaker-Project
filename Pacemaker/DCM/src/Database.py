from src.Password import Password
from src.Pacemaker import Pacemaker
from src.User import User
import json

class usernameExists(Exception):

    def __init__(self, message="Username already exists\n"):
        self.message=message
        super().__init__(self.message)

class Database:

    def __init__(self,fileName):
        self.count = 0
        self.emailcheck = 'valid'
        self.fileName=fileName
        self.data={}
        self.file=open(fileName,'r+')    #open the file
        try:
            self.data = json.loads(self.file.read())
            #print("\n self.data:    ", self.data)
        except json.decoder.JSONDecodeError:
            print('File is empty')
        self.file.close()


    def addUser(self,user,pacemaker=Pacemaker()):
        self.count = 0

        """if username or email exists, do not proceed with addtion of user"""
        for dict in self.data:
            self.count += 1
            if user.email == self.data[dict]['email']: 
                return 3    #email taken

            if (user.username == dict): #if the username or email is taken
                return 1    #username taken
        
        if self.count >= 10:
            return 2    #database full

        self.file=open(self.fileName,'r+')    #open the file
        try:
            self.data = json.loads(self.file.read())
            #print(self.data)
        except json.decoder.JSONDecodeError:
            print('File is empty')

        """initialize user data in database"""
        self.data[user.username]={}
        self.data[user.username]["username"]=user.username
        self.data[user.username]["password"]=user.passwordHash
        self.data[user.username]["firstName"]=user.firstName
        self.data[user.username]["lastName"]=user.lastName
        self.data[user.username]["email"]=user.email
        #----------------------------------------------ADD user settings that are empty since this is a new account (added in save())
        self.data[user.username]["pacemakerSettings"]={}
        self.data[user.username]["pacemakerSettings"]["currentMode"]="AOO"

        self.data[user.username]["pacemakerSettings"]["AOO"]={}
        self.data[user.username]["pacemakerSettings"]["VOO"]={}
        self.data[user.username]["pacemakerSettings"]["VVI"]={}
        self.data[user.username]["pacemakerSettings"]["AAI"]={}
        self.data[user.username]["pacemakerSettings"]["AOOR"]={}
        self.data[user.username]["pacemakerSettings"]["VOOR"]={}
        self.data[user.username]["pacemakerSettings"]["AAIR"]={}
        self.data[user.username]["pacemakerSettings"]["VVIR"]={}


        ##

        self.data[user.username]["pacemakerSettings"]["AOO"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["AOO"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["AOO"]["atrialAmplitude"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["VOO"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["VOO"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["AAI"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["RP"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["PVARP"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["hysteresis"]=0
        self.data[user.username]["pacemakerSettings"]["AAI"]["rateSmoothing"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["VVI"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["RP"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["hysteresis"]=0
        self.data[user.username]["pacemakerSettings"]["VVI"]["rateSmoothing"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["AOOR"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["activityThreshold"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["reactionTime"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["responseFactor"]=0
        self.data[user.username]["pacemakerSettings"]["AOOR"]["recoveryTime"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["VOOR"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["activityThreshold"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["reactionTime"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["responseFactor"]=0
        self.data[user.username]["pacemakerSettings"]["VOOR"]["recoveryTime"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["AAIR"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["maximumSensorRate"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["atrialAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["atrialPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["atrialSensitivity"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["RP"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["PVARP"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["hysteresis"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["rateSmoothing"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["activityThreshold"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["reactionTime"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["responseFactor"]=0
        self.data[user.username]["pacemakerSettings"]["AAIR"]["recoveryTime"]=0
        ##
        self.data[user.username]["pacemakerSettings"]["VVIR"]["upperRate"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["lowerRate"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["maximumSensorRate"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["ventricularAmplitude"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["ventricularPulseWidth"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["ventricularSensitivity"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["RP"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["hysteresis"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["rateSmoothing"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["activityThreshold"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["reactionTime"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["responseFactor"]=0
        self.data[user.username]["pacemakerSettings"]["VVIR"]["recoveryTime"]=0

        self.updateDatabase()
        self.file.close()
        
        return 0
            
    
    def updateDatabase(self):   #this is the function that does the actual writing. "updatePacemaker(self,user,pacemaker)" (below) is what you are looking for
        """writes user to the database, aka, the json file"""
        self.file.seek(0)
        self.file.truncate()
        json.dump(self.data,self.file,indent=4)


    def doLogin(self,usernameStr,passwordHash):
        if(usernameStr not in self.data):
            print("User doesnt exist")
            return False    #user doesnt exist
        elif(self.data[usernameStr]["password"]==passwordHash):
            print("Success!")
            return True #login successful
        else:
            print("Incorrect password")
            return False    #incorrect password

    def updateAOO(self,user,pacemaker):
        try:
            self.data[user]["pacemakerSettings"]["AOO"]["pacingMode"]=pacemaker.pacingMode
            self.data[user]["pacemakerSettings"]["AOO"]["upperRate"]=int(pacemaker.upperRate)
            self.data[user]["pacemakerSettings"]["AOO"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["AOO"]["atrialAmplitude"]=float(pacemaker.amplitude)

        except:
            self.data[user]["pacemakerSettings"]["AOO"]["pacingMode"]=""
            self.data[user]["pacemakerSettings"]["AOO"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["AOO"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["AOO"]["atrialAmplitude"]=0

    def updateVOO(self,user,pacemaker):
        try:
            self.data[user]["pacemakerSettings"]["VOO"]["pacingMode"]=pacemaker.pacingMode
            self.data[user]["pacemakerSettings"]["VOO"]["upperRate"]=int(pacemaker.upperRate)
            self.data[user]["pacemakerSettings"]["VOO"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]=float(pacemaker.amplitude)
        except:
            self.data[user]["pacemakerSettings"]["VOO"]["pacingMode"]=""
            self.data[user]["pacemakerSettings"]["VOO"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["VOO"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]=0

    def updateVVI(self,user,pacemaker):
        try:
            self.data[user]["pacemakerSettings"]["VVI"]["upperRate"]=int(pacemaker.upperRate)
            self.data[user]["pacemakerSettings"]["VVI"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]=float(pacemaker.amplitude)
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]=float(pacemaker.sensitivity)
            self.data[user]["pacemakerSettings"]["VVI"]["RP"]=float(pacemaker.RP)
            self.data[user]["pacemakerSettings"]["VVI"]["hysteresis"]=pacemaker.hysteresis
            self.data[user]["pacemakerSettings"]["VVI"]["rateSmoothing"]=float(pacemaker.smoothing)

        except:
            self.data[user]["pacemakerSettings"]["VVI"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["RP"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["hysteresis"]=0
            self.data[user]["pacemakerSettings"]["VVI"]["rateSmoothing"]=0

    def updateAAI(self,user,pacemaker):
        try:
            self.data[user]["pacemakerSettings"]["AAI"]["upperRate"]=int(pacemaker.upperRate)
            self.data[user]["pacemakerSettings"]["AAI"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["AAI"]["atrialAmplitude"]=float(pacemaker.amplitude)
            self.data[user]["pacemakerSettings"]["AAI"]["atrialSensitivity"]=float(pacemaker.sensitivity)
            self.data[user]["pacemakerSettings"]["AAI"]["RP"]=float(pacemaker.RP)
            self.data[user]["pacemakerSettings"]["AAI"]["PVARP"]=float(pacemaker.PVARP)
            self.data[user]["pacemakerSettings"]["AAI"]["hysteresis"]=pacemaker.hysteresis
            self.data[user]["pacemakerSettings"]["AAI"]["rateSmoothing"]=float(pacemaker.smoothing)

        except:
            self.data[user]["pacemakerSettings"]["AAI"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["atrialAmplitude"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["atrialSensitivity"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["RP"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["PVARP"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["hysteresis"]=0
            self.data[user]["pacemakerSettings"]["AAI"]["rateSmoothing"]=0


    def updateAOOR(self,user,pacemaker):

        try:
            print("saving AOOR")

            self.data[user]["pacemakerSettings"]["AOOR"]["upperRate"]=int(pacemaker.upperRate)
            
            self.data[user]["pacemakerSettings"]["AOOR"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]=int(pacemaker.maximumSensorRate)
            self.data[user]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]=float(pacemaker.amplitude)
            self.data[user]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["AOOR"]["activityThreshold"]=float(pacemaker.activityThreshold)
            self.data[user]["pacemakerSettings"]["AOOR"]["reactionTime"]=int(pacemaker.reactionTime)
            self.data[user]["pacemakerSettings"]["AOOR"]["responseFactor"]=int(pacemaker.responseFactor)
            self.data[user]["pacemakerSettings"]["AOOR"]["recoveryTime"]=int(pacemaker.recoveryTime)
            
            print("saved AOOR")
        except:
            self.data[user]["pacemakerSettings"]["AOOR"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["activityThreshold"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["reactionTime"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["responseFactor"]=0
            self.data[user]["pacemakerSettings"]["AOOR"]["recoveryTime"]=0


    def updateVOOR(self,user,pacemaker):

        try:
            print("saving VOOR")

            self.data[user]["pacemakerSettings"]["VOOR"]["upperRate"]=int(pacemaker.upperRate)
            self.data[user]["pacemakerSettings"]["VOOR"]["lowerRate"]=int(pacemaker.lowerRate)
            self.data[user]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]=int(pacemaker.maximumSensorRate)
            self.data[user]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]=float(pacemaker.amplitude)
            self.data[user]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]=int(pacemaker.pulseWidth)
            self.data[user]["pacemakerSettings"]["VOOR"]["activityThreshold"]=float(pacemaker.activityThreshold)
            self.data[user]["pacemakerSettings"]["VOOR"]["reactionTime"]=int(pacemaker.reactionTime)
            self.data[user]["pacemakerSettings"]["VOOR"]["responseFactor"]=int(pacemaker.responseFactor)
            self.data[user]["pacemakerSettings"]["VOOR"]["recoveryTime"]=int(pacemaker.recoveryTime)
            
        except:
            self.data[user]["pacemakerSettings"]["VOOR"]["upperRate"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["lowerRate"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["activityThreshold"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["reactionTime"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["responseFactor"]=0
            self.data[user]["pacemakerSettings"]["VOOR"]["recoveryTime"]=0



    def updatePacemaker(self,user,pacemaker):
        """update the pacemaker settings in the JSON file"""
        
        self.file=open(self.fileName,'r+')    #open the file

        try:    #read the JSON file to get its current contents in the form of a dict
            self.data = json.loads(self.file.read())
            #print(self.data)
        except json.decoder.JSONDecodeError:    #reading returns an error...
            print('File is empty')
    
        self.data[user]["pacemakerSettings"]["currentMode"]=pacemaker.pacingMode    # update current pacing mode.
        #ie, the line "currentMode": "AAI", in the dict. 

        if(pacemaker.pacingMode=="AOO"):    #This is where the corresponding mode for the user is updated
            self.updateAOO(user,pacemaker)  #
        elif(pacemaker.pacingMode=="VOO"):
            self.updateVOO(user,pacemaker)
            pass
        elif(pacemaker.pacingMode=="AAI"):
            self.updateAAI(user,pacemaker)
            pass
        elif(pacemaker.pacingMode=="VVI"):
            self.updateVVI(user,pacemaker)
            pass      
        elif(pacemaker.pacingMode=="AOOR"):
            self.updateAOOR(user,pacemaker)
            pass    
        elif(pacemaker.pacingMode=="VOOR"):
            self.updateVOOR(user,pacemaker)
            pass    



        self.updateDatabase()
        self.file.close()

        pass
