from mongoengine import *

class Tweet(Document):
    tweetId = StringField(Required=True, primary_key=True)
    username = StringField(Required=True)
    tweetBody = StringField()
    date = StringField(Required=True)
    is_fake = StringField(Required=True)
