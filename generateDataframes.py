from Mongo.MongoActions import MongoActions
from mongoengine import connect
import os

connect(host= str(os.environ.get("FAKE")))
mongoActions = MongoActions()
mongoActions.generate_user_tweets_dataframe()