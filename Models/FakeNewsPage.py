from mongoengine import *

class FakeNewsPage(Document):
    head = StringField(required=True)
