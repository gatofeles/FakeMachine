from re import T
from mongoengine import *

class UserTweets(Document):   
    tweetId = StringField(required=True, primary_key=True)
    username = StringField(required=True)
    tweetBody = StringField(required=True)