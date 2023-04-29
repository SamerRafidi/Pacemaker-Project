from Database import Database
from Pacemaker import Pacemaker
from Username import Username
from Password import Password
from User import User
from Utils import special_characters
filename='DCMV2/src/data_base.json'

database=Database('DCMV2/src/data_base.json')

username=Username("hakam")
password1=Password("Password123")
pacemaker1=Pacemaker()

user1=User(username,password1,pacemaker1)

print(username.username," ",password1.passwordHash," ",pacemaker1)

database.add(user1)

username2=Username("sinan")
password2=Password("password123")
pacemaker2=Pacemaker()

user1=User(username2,password1,pacemaker1)

print(username.username," ",password1.passwordHash," ",pacemaker1)

database.add(user1)

