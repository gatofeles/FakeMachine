from mongoengine import *

class User(Document):
   
    username = StringField(required=True, primary_key=True)
    profileLink = StringField(required=True)
    birthdate = StringField(default ='')
    joinDate = StringField(default ='')
    description = StringField(default ='')
    location = StringField(default='')
    following = StringField(default='')
    followers = StringField(default='')


