from re import T
from mongoengine import *

class UserMsg(Document):   
    tweetId = StringField(required=True, primary_key=True)
    username = StringField(required=True)
    tweetBody = StringField(required=True)