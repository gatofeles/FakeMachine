from Models.User import User
from Models.Tweet import Tweet
from Models.Event import Event
from Models.FakeNewsPage import FakeNewsPage
from Models.UserMsg import UserMsg
from Models.UserTweets import UserTweets
import pandas as pd

class MongoActions:
    def createUser(username, profileLink, description, joinDate, location, following, followers, birthdate) -> User:
        user = User()
        user.username = username
        user.profileLink = profileLink
        user.description = description
        user.joinDate = joinDate
        user.location = location
        user.followers = followers
        user.following = following
        user.birthdate = birthdate

        user.save()
        return user

    def createTweet(tweetId, tweetBody, userName, date, is_fake='true')->Tweet:
        tweet = Tweet()
        tweet.tweetId = tweetId
        tweet.tweetBody = tweetBody
        tweet.username = userName
        tweet.date = date
        tweet.is_fake = is_fake

        tweet.save()
        return tweet

    def create_event(tweetId, username, event_type)->Event:
        event = Event()
        event.event_type = event_type
        event.username = username
        event.tweet_id = tweetId

        event.save()
        return event

    def find_event(tweetId, username, event_type)->Event:
        querry = Event.objects(tweet_id=tweetId, username=username, event_type=event_type).first()
        return querry

    def findUserByName(username) -> User:
        querry = User.objects(username=username).first()
        return querry
    
    def get_all_users(self):
        querry = User.objects
        return querry
    
    def get_user_msg(id) -> UserMsg:
        querry = UserMsg.objects(tweetId = id)
        return querry

    def count_all_user_msg(username)->UserMsg:
        query = UserMsg.objects(username= username).count()
        return query
    
    def create_user_msg(tweetId, tweetBody, username) -> UserMsg:
        user_msg = UserMsg()
        msg_check = UserMsg.objects(tweetId = tweetId).first()
        if(msg_check):
            return
        else:
            user_msg.tweetId = tweetId
            user_msg.tweetBody = tweetBody
            user_msg.username = username
            user_msg.save()
        
        return user_msg
        
    def findTweetById(tweetId) -> Tweet:
        querry = Tweet.objects(tweetId=tweetId).first()
        return querry

    def find_head_by_quote(self, quote) -> FakeNewsPage:
        querry = FakeNewsPage.objects(head=quote).first()
        return querry

    def register_header(self, quote):
        fake_news_page = FakeNewsPage()
        fake_news_page.head = quote
        fake_news_page.save()
        
    def create_user_tweets(self, tweetId, tweetBody, username) -> UserTweets:
        user_msg = UserTweets()
        msg_check = UserTweets.objects(tweetId = tweetId).first()
        if(msg_check):
            return
        else:
            user_msg.tweetId = tweetId
            user_msg.tweetBody = tweetBody
            user_msg.username = username
            user_msg.save()
        
        return user_msg
    
    def get_user_tweets(id) -> UserTweets:
        query = UserTweets.objects(tweetId = id)
        return query

    def count_all_user_tweets(self, username) -> UserTweets:
        query = UserTweets.objects(username= username).count()
        return query
    
    def get_all_user_tweets(username) -> UserTweets:
        query = UserTweets.objects(username= username)
        return query
    
    def format_follow(self, follow):
        if follow != None and follow != '':
            faux = follow.split()[0]  
            if "M" in faux:
                cut = faux.replace("M", "")
                return float(cut)*1000000
            elif "K" in faux:
                cut = faux.replace("K", "")
                return float(cut)*1000
            else:
                if ',' in faux:
                    faux = faux.replace(",", "")
                try:
                    return float(faux)
                except:
                    return 0
        else:
            return 0


    
    def generate_user_info_dataframe(self):
        usersDic = {'username':[], 'followers':[], 'following':[], 'location':[]}
        users = self.get_all_users()
        for user in users:
            usersDic['username'].append(user.username)
            usersDic['followers'].append(self.format_follow(user.followers))
            usersDic['following'].append(self.format_follow(user.following))
            usersDic['location'].append(str(user.location))
        df = pd.DataFrame(usersDic)
        df.to_csv('usersTru_str', index=False)
                          
                
    
    def generate_user_tweets_dataframe(self)-> UserTweets:
        userTweetsDic = {'string':[]}
        users = self.get_all_users()
        count = 0
        for user in users:
            query = UserTweets.objects(username = user.username)
            corpus = ""
            
            for tweet in query:
                corpus += tweet.tweetBody
            userTweetsDic['string'].append(corpus) 
            count += 1
            if count > 5000:
                break
          
            
        df = pd.DataFrame(userTweetsDic)
        df.to_csv('userTweetsTrue_str', index=False)

                
        
