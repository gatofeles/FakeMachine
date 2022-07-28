import tweepy
import os
from mongoengine import connect
from Mongo.MongoActions import MongoActions
import time
class TweetApi:
    def __init__(self):
        
        connect(host= str(os.environ.get("FAKE")))
        self.client = tweepy.Client(bearer_token="--token--", consumer_key="--key--", consumer_secret="--secret--", access_token="--token", access_token_secret="--secret--")
        self.mongoActions = MongoActions()
        
    def get_user_info(self, out_username):
        tries = 0

        while tries < 5:
            try:        
                return self.client.get_user(username = out_username)
                
            except:
                tries+=1
                time.sleep(1) 
        
    def get_users_tweets(self):
        print("Connected on host "+str(os.environ.get("FAKE")))
        users = self.mongoActions.get_all_users()
        for user in users:
            if self.mongoActions.count_all_user_tweets(username=user.username) <= 0:
                userInfo = self.get_user_info(user.username) 
                if userInfo.data != None:
                    tweets = self.client.get_users_tweets(userInfo.data.id)
                    if tweets.data != None:
                        for tweet in tweets.data:
                            if tweet != None:
                                self.mongoActions.create_user_tweets(tweetId=tweet.data["id"], tweetBody=tweet.data["text"], username=user.username)
    

        