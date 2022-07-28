from mongoengine import *

class Event(Document):
    event_type = StringField(required=True)
    username = StringField(required=True)
    tweet_id = StringField(required=True)