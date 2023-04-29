from click import password_option
from flask import Flask, render_template, request, redirect
import hashlib
from src.Database import Database
from src.Pacemaker import Pacemaker
from src.Username import Username
from src.Password import Password
from src.User import User
from threading import Thread
from src.serialCom import SerialCom

from src.Graph import ECGGraph

import threading
import asyncio
import time
from flask import Flask


import sys
app=Flask(__name__)
filename='src/data_base.json'



connectionStatus="Disconnected"
comPort="NA"
serialNumber="000000000000"



# this is the "main" file
# all HTML files go in the templates/ directory as required by flask
# all CSS files go in the static/styles/ directory as required by flask

database=Database(filename)
terminal="Logged in"
box0=-1
box1=-1
box2=-1
box3=-1
box4=-1
box5=-1
box6=-1
box7=-1
box8=-1
box9=-1
box10=-1

global currentMode

currentMode=""

serialcom = SerialCom()

@app.route('/') ##default function called when you load the page. This one just takes #you to the home screen
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST']) ##default function called when you load the page. This one just takes #you to the home screen
def login():
    
    print("\n\nLogin query")
    # username = request.form['username']
    # print("Username: ",username,"\n")
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/NewUser/', methods = ['GET', 'POST'])
def NewUser(): #function that adds new users data 
    errormsg = ''
    """Registration form"""
    username = Username(request.form['username'])
    password = Password(request.form['password'])

    #Check if username is valid
    if username.performValidation(username.username):
        firstName = request.form['firstname']
        lastName = request.form['lastname']
        email = request.form['email']
    else: #if not, send that msg to the front end
        return render_template("register.html", errormsg = "Invalid Username",terminal=terminal)

    user=User(username,password,firstName,lastName,email)
    #print(database.add(user))

    #this peice of code adds the user to the data base twice. 
    #a user is added during the if statement, and again in the body of the condition
    #not ideal for obvious reasons 

    addUserErrorCode=database.addUser(user)

    if (addUserErrorCode==0): # can add user (no error)
        print("USER WAS VALID")
        database.addUser(user)
        return render_template('index.html')
    elif (addUserErrorCode==1): #username is taken
        print("USERNAME TAKEN")
        return render_template('register.html', errormsg = "taken")
    elif (addUserErrorCode==2): #database is full
        print("count = ", database.count)
        return render_template('register.html', errormsg = "datafull")
    elif (addUserErrorCode==3): # email in use
        print("EMAIL TAKEN")
        return render_template('register.html', errormsg = 'bademail')




userSave = ''

@app.route('/ExistingUser/', methods = ['GET', 'POST'])
def ExistingUser():
    global userSave
    username = request.form['username']
    password = request.form['password']
    passwordHash=hashlib.sha224(bytes(password,'ascii')).hexdigest()
    global currentMode
    currentMode="AOO"

    if (database.doLogin(username,passwordHash) == True):
        userSave = username
        # return render_template('UserPage.html',user=username, pacingMode="AOO",terminal="Logged in")    #change to the main user page
        return render_template("AOO.html", saved = "true",user=userSave, pacingMode="AOO", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AOO"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AOO"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )
    else:
        return render_template('index.html', errormsg = "wrong",terminal="Logged in")    #redirect to main page (or just keep on the same page ig)


@app.route('/Register/', methods = ['GET', 'POST'])
def Register():

    return render_template('register.html')


#Adds a button that displays if we're connected to device
@app.route('/connect', methods = ['GET', 'POST'])
def isconnect():

    global serialcom
    global comPort
    global connectionStatus
    global serialNumber
    
    username = userSave # get logged in user's username
    pacingMode = "" # the mode currently being programmed

    try:
        connectionInfo=serialcom.openCOM()
        print(connectionInfo[0])
        print(connectionInfo[1])
        terminal="Connection successful"
        comPort=connectionInfo[1]
        serialNumber=connectionInfo[0]
        connectionStatus="Connected"

    except:
        terminal="Connection unsuccessful. Please try again"
        comPort="NA"
        serialNumber="000000000000"
        connectionStatus="Disconnected"


    #ECG=ECGGraph()


    print("Current mode: ", currentMode)




    if(currentMode=="AOO"):
        return goAOO(terminal)
    elif(currentMode=="VOO"):
       return goVOO(terminal)
    elif(currentMode=="VVI"):
       return goVVI(terminal)
    elif(currentMode=="AAI"):
       return goAAI(terminal)
    elif(currentMode=="AOOR"):
       return goAOOR(terminal)
    elif(currentMode=="VOOR"):
       return goVOOR(terminal)



#Save user data to backend (json file)
def save(pacingMode):
    username = userSave 
    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']

    print(username)

    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth)
    database.updatePacemaker(username,pacemaker)
    print('saved successfully')
    return render_template(pacingMode+".html", saved = "true",user=userSave, pacingMode=pacingMode,terminal=terminal)



@app.route('/saveAOO', methods = ['GET', 'POST'])
def saveAOO(): 
    username = userSave # get logged in user's username
    pacingMode = "AOO" # the mode currently being programmed
    upperRate = request.form['upper_rate']  #from the form, request (GET) the data
    lowerRate = request.form['low_rate']

    print("upper", upperRate)
    print("lower", lowerRate)


    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']

    print(username)

    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth)    #Pacemaker is just a class that encapsulates (contains) the pacemaker data.
    #the pacemaker class will pass the above values to the members in the class. 
    #the members that are not passed anything will default to -1 (this happens in the Pacemaker class)
    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else:
        print('saved successfully')
        database.updatePacemaker(username,pacemaker)    # update the pacemaker settings for this particular user
        #more about the above line in the database updatePacemaker file

        terminal="AOO saved successfully"
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode  #lets the system know what was just programmed for this user


    #passes these variables to the html file using flask
    return render_template("AOO.html", saved = "true",user=userSave, pacingMode=pacingMode, terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AOO"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AOO"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    
    )

def goAOO(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "AOO" # the mode currently being programmed
    return render_template("AOO.html", saved = "true",user=userSave, pacingMode=pacingMode, terminal=_terminal,database=database.data,
                            box0=str(database.data[username]["pacemakerSettings"]["AOO"]["upperRate"]),
                            box1=str(database.data[username]["pacemakerSettings"]["AOO"]["lowerRate"]),
                            box2=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialAmplitude"]),
                            box3=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]),
                            comPort=comPort,
                            serialNumber=serialNumber,
                            connectionStatus=connectionStatus
                            )



@app.route('/saveVOO', methods = ['GET', 'POST'])
def saveVOO(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    username = userSave 
    pacingMode = "VOO"
    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']



    print(username)

    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth)
    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else:
        print('saved successfully')
        database.updatePacemaker(username,pacemaker)

        terminal="VOO saved successfully"
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode


    return render_template("VOO.html", saved = "true",user=userSave, pacingMode=pacingMode, terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOO"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOO"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )

def goVOO(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "VOO" # the mode currently being programmed
    return render_template("VOO.html", saved = "true",user=userSave, pacingMode=pacingMode, terminal=_terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOO"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOO"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )






# 
@app.route('/saveVVI', methods = ['GET', 'POST'])
def saveVVI(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    username = userSave 
    pacingMode = "VVI"

    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']
    sensitivity = request.form['sensitivity']
    RP = request.form['RP']

    try:
        hysteresis = request.form['hysteresis']
    except:
        hysteresis="off"

    smoothing = request.form['smoothing']

    print(username)

    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth,sensitivity,RP,hysteresis,smoothing)

    print(lowerRate, upperRate)
    print('saved successfully')
    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else: 
        print('saved successfully')
        terminal="Saved successfully"

        database.updatePacemaker(username,pacemaker)
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode



    return render_template("VVI.html", saved = "true",user=userSave, pacingMode="VVI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VVI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VVI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["VVI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["VVI"]["hysteresis"]),
        box7=str(database.data[username]["pacemakerSettings"]["VVI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )

def goVVI(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "VVI" # the mode currently being programmed
    return render_template("VVI.html", saved = "true",user=userSave, pacingMode="VVI", terminal=_terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VVI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VVI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["VVI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["VVI"]["hysteresis"]),
        box7=str(database.data[username]["pacemakerSettings"]["VVI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )


@app.route('/saveAAI', methods = ['GET', 'POST'])
def saveAAI(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    username = userSave 
    pacingMode = "AAI"

    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']
    sensitivity = request.form['sensitivity']
    RP = request.form['RP']
    PVARP = request.form['PVARP']

    try:
        hysteresis = request.form['hysteresis']
    except:
        hysteresis="off"

    smoothing = request.form['smoothing']


    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth,sensitivity,RP,hysteresis,smoothing,PVARP)

    print(lowerRate, upperRate)
    print('saved successfully')
    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else: 
        print('saved successfully')
        terminal="Saved successfully"

        database.updatePacemaker(username,pacemaker)
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode




    return render_template("AAI.html", saved = "true",user=userSave, pacingMode="AAI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AAI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AAI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["AAI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["AAI"]["PVARP"]),

        box7=str(database.data[username]["pacemakerSettings"]["AAI"]["hysteresis"]),
        box8=str(database.data[username]["pacemakerSettings"]["AAI"]["rateSmoothing"]),

        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )

def goAAI(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "AAI" # the mode currently being programmed
    return render_template("AAI.html", saved = "true",user=userSave, pacingMode="AAI", terminal=_terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AAI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AAI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["AAI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["AAI"]["PVARP"]),

        box7=str(database.data[username]["pacemakerSettings"]["AAI"]["hysteresis"]),
        box8=str(database.data[username]["pacemakerSettings"]["AAI"]["rateSmoothing"]),

        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus

    )


##new mode saving below
@app.route('/saveAOOR', methods = ['GET', 'POST'])
def saveAOOR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Saving AOOR")
   
   
   
    username = userSave 
    pacingMode = "AOOR"


    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    maximumSensorRate=request.form['maximumSensorRate']
    pulseWidth=request.form['pulse_width']
    activityThreshold=request.form['activity_threshold']
    reactionTime=request.form['reaction_time']
    responseFactor=request.form['response_factor']
    recoveryTime=request.form['recovery_time']


    print(username)

    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth,None,None,None,None,None,
                        maximumSensorRate,activityThreshold,reactionTime,responseFactor,recoveryTime)

    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else: 
        print('saved successfully')
        terminal="Saved successfully"

        database.updatePacemaker(username,pacemaker)
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode


    return render_template("AOOR.html", saved = "true",user=userSave, pacingMode="AOOR", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["AOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["AOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["AOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["AOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )


def goAOOR(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "AOOR" # the mode currently being programmed
    return render_template("AOOR.html", saved = "true",user=userSave, pacingMode="AOOR", terminal=_terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["AOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["AOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["AOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["AOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )


@app.route('/saveVOOR', methods = ['GET', 'POST'])
def saveVOOR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Saving VOOR")
   
   
   
    username = userSave 
    pacingMode = "VOOR"


    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    maximumSensorRate=request.form['maximumSensorRate']
    pulseWidth=request.form['pulse_width']
    activityThreshold=request.form['activity_threshold']
    reactionTime=request.form['reaction_time']
    responseFactor=request.form['response_factor']
    recoveryTime=request.form['recovery_time']


    print(username)

    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth,None,None,None,None,None,
                        maximumSensorRate,activityThreshold,reactionTime,responseFactor,recoveryTime)
    
    if(int(lowerRate or 0)>int(upperRate or 0)):
        terminal="Error. Rate crossing or invalid rate"
    else: 
        print('saved successfully')
        terminal="Saved successfully"

        database.updatePacemaker(username,pacemaker)
        database.data[username]["pacemakerSettings"]["currentMode"]=pacingMode


    return render_template("VOOR.html", saved = "true",user=userSave, pacingMode="VOOR", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["VOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["VOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["VOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["VOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )


def goVOOR(_terminal):
    username = userSave # get logged in user's username
    pacingMode = "VOOR" # the mode currently being programmed
    return render_template("VOOR.html", saved = "true",user=userSave, pacingMode="VOOR", terminal=_terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["VOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["VOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["VOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["VOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus

    )


@app.route('/updatePacingForm', methods = ['GET', 'POST'])
def updatePacingForm(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    username = userSave 
    pacingMode = request.form['pacingmode']
    upperRate = request.form['upper_rate']
    lowerRate = request.form['low_rate']
    amplitude = request.form['amplitude']
    pulseWidth = request.form['pulse_width']


    #will likely need to be expanded in the future. 
    #try to come up with a scalable way to do this. 
    #consider if we have 40 params we need to program. How would we do that?
    pacemaker=Pacemaker(pacingMode,upperRate,lowerRate,amplitude,pulseWidth)
    
    database.updatePacemaker(username,pacemaker)

    print('Updated pacing mode successfully')

    return render_template((pacingMode+".html"), saved = "true",user=userSave, pacingMode=pacingMode,terminal=terminal)


@app.route('/logout', methods = ['GET', 'POST'])
def logout(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("User logged out")

    return render_template("index.html")











""" RE DIRECTION FUNCTIONS 
    These functions allow the user to navitage the different pacing modes.
    They also fetch data from the database to display in the textbox...
"""

@app.route('/redirectVOO', methods = ['GET'])
def redirectVOO(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect VOO")
    terminal="Redirect VOO"
    username = userSave 
    global currentMode
    currentMode="VOO"


    return render_template("VOO.html", saved = "true",user=userSave, pacingMode="VOO", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOO"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOO"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOO"]["ventricularPulseWidth"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
        
    )


@app.route('/redirectAOO', methods = ['GET'])
def redirectAOO(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect AOO")
    terminal="Redirect AOO"
    username = userSave 
    global currentMode
    currentMode="AOO"

    return render_template("AOO.html", saved = "true",user=userSave, pacingMode="AOO", terminal=terminal,database=database.data,
    box0=str(database.data[username]["pacemakerSettings"]["AOO"]["upperRate"]),
    box1=str(database.data[username]["pacemakerSettings"]["AOO"]["lowerRate"]),
    box2=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialAmplitude"]),
    box3=str(database.data[username]["pacemakerSettings"]["AOO"]["atrialPulseWidth"]),
    comPort=comPort,
    serialNumber=serialNumber,
    connectionStatus=connectionStatus
)




@app.route('/redirectVVI', methods = ['GET'])
def redirectVVI(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect VVI")
    terminal="Redirect VVI"
    username = userSave 
    global currentMode
    currentMode="VVI"



    return render_template("VVI.html", saved = "true",user=userSave, pacingMode="VVI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VVI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VVI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["VVI"]["ventricularSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["VVI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["VVI"]["hysteresis"]),
        box7=str(database.data[username]["pacemakerSettings"]["VVI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )

@app.route('/redirectAAI', methods = ['GET'])
def redirectAAI(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect AAI")
    terminal="Redirect AII"
    username = userSave 
    global currentMode
    currentMode="AAI"




    return render_template("AAI.html", saved = "true",user=userSave, pacingMode="AAI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AAI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AAI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["AAI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["AAI"]["PVARP"]),

        box7=str(database.data[username]["pacemakerSettings"]["AAI"]["hysteresis"]),
        box8=str(database.data[username]["pacemakerSettings"]["AAI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )




#CHANGE THE ONES BELOW. ThE ONES ABOVE WORK
@app.route('/redirectAOOR', methods = ['GET'])
def redirectAOOR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect AOOR")
    terminal="Redirect AOOR"
    username = userSave 
    global currentMode
    currentMode="AOOR"



    return render_template("AOOR.html", saved = "true",user=userSave, pacingMode="AOOR", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["AOOR"]["atrialPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["AOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["AOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["AOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["AOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus

    )

@app.route('/redirectVOOR', methods = ['GET'])
def redirectVOOR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect VOOR")
    terminal="Redirect VOOR"
    username = userSave 
    global currentMode
    currentMode="VOOR"


    return render_template("VOOR.html", saved = "true",user=userSave, pacingMode="VOOR", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["VOOR"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["VOOR"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["VOOR"]["maximumSensorRate"]),
        box3=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularAmplitude"]),
        box4=str(database.data[username]["pacemakerSettings"]["VOOR"]["ventricularPulseWidth"]),
        box5=str(database.data[username]["pacemakerSettings"]["VOOR"]["activityThreshold"]),
        box6=str(database.data[username]["pacemakerSettings"]["VOOR"]["reactionTime"]),
        box7=str(database.data[username]["pacemakerSettings"]["VOOR"]["responseFactor"]),
        box8=str(database.data[username]["pacemakerSettings"]["VOOR"]["recoveryTime"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus

    )


@app.route('/redirectAAIR', methods = ['GET'])
def redirectAAIR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect AAIR")
    terminal="Redirect AAIR"
    username = userSave 
    global currentMode
    currentMode="AAIR"



    return render_template("AAIR.html", saved = "true",user=userSave, pacingMode="AAI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AAI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AAI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["AAI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["AAI"]["PVARP"]),

        box7=str(database.data[username]["pacemakerSettings"]["AAI"]["hysteresis"]),
        box8=str(database.data[username]["pacemakerSettings"]["AAI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )

@app.route('/redirectVVIR', methods = ['GET'])
def redirectVVIR(): #Function works for the most part, only problem is it adds uneccessary characters at the end of json file. *Don't know the cause yet*
    print("Redirect VVIR")
    terminal="Redirect VVIR"
    username = userSave 
    global currentMode
    currentMode="VVIR"



    return render_template("VVIR.html", saved = "true",user=userSave, pacingMode="AAI", terminal=terminal,database=database.data,
        box0=str(database.data[username]["pacemakerSettings"]["AAI"]["upperRate"]),
        box1=str(database.data[username]["pacemakerSettings"]["AAI"]["lowerRate"]),
        box2=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialAmplitude"]),
        box3=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialPulseWidth"]),

        box4=str(database.data[username]["pacemakerSettings"]["AAI"]["atrialSensitivity"]),
        box5=str(database.data[username]["pacemakerSettings"]["AAI"]["RP"]),
        box6=str(database.data[username]["pacemakerSettings"]["AAI"]["PVARP"]),

        box7=str(database.data[username]["pacemakerSettings"]["AAI"]["hysteresis"]),
        box8=str(database.data[username]["pacemakerSettings"]["AAI"]["rateSmoothing"]),
        comPort=comPort,
        serialNumber=serialNumber,
        connectionStatus=connectionStatus
    )


def background_task():
    ECG=ECGGraph()


    
##function for loading and running the pacemaker. 
#serial communication happens here
@app.route('/run', methods = ['GET', 'POST'])
def loadAndRun():

    #t=threading.Thread(target=background_task)
    #t.start()

    username = userSave 

    global serialcom
    global terminal




    print("Current mode: ", currentMode)


    pacemaker = Pacemaker()
    username = userSave # get logged in user's username
    pacingMode = "" # the mode currently being programmed

    try:
        serialcom.updateParams(currentMode,username)
        print("send failed")

        serialcom.send()
        terminal="Load successful. Now running "+currentMode

    except:
        terminal="Load unsuccessful. Please try again"




    if(currentMode=="AOO"):
        return goAOO(terminal)
    elif(currentMode=="VOO"):
       return goVOO(terminal)
    elif(currentMode=="VVI"):
       return goVVI(terminal)
    elif(currentMode=="AAI"):
       return goAAI(terminal)
    elif(currentMode=="AOOR"):
       return goAOOR(terminal)
    elif(currentMode=="VOOR"):
       return goVOOR(terminal)





    
        


#app.run()

print('running')

if __name__ == "__main__":
    app.run()
