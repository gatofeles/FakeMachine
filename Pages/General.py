from ast import Assert
from multiprocessing import cpu_count
from typing import BinaryIO
from selenium.webdriver.common.keys import Keys
import Helpers.Wait as hw
from Mongo.MongoActions import MongoActions
from Helpers.DriverHandle import DriverHandle
import time
import Pages.Login as pl
from selenium.webdriver.common.action_chains import ActionChains

class General:

    def __init__(self, webdriver):
        self.chromeDriver = webdriver
        self.likes_qtd = 0
        self.shares_qtd = 0
        self.wait = hw.Wait(webdriver)
        self.searchBtnXpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div'
        self.searchFieldXpath = '//*[@data-testid="SearchBox_Search_Input"]'
        self.teewtsConteinerXpath = '//*[@data-testid="primaryColumn"]//*/div[contains(@aria-label, "Timeline")]'
        self.tweetContentXpath = '//*[@class = "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]'
        self.userDescriptionXpath = '//*[@data-testid="UserDescription"]'
        self.location_xpath = '//*[@data-testid="UserLocation"]'
        self.user_birthdate_xpath = '//*[@data-testid="UserBirthdate"]'
        self.userHeadInfoXpath = '//*[@data-testid= "UserProfileHeader_Items"]'
        self.userJoinLocationXpath = '//*[@class = "css-901oao css-16my406 r-14j79pv r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0"]'
        self.latestBtnXpath = "//*[contains(text(), 'Mais recentes')]"
        self.optionBtnXpath = '//*[@data-testid= "searchBoxOverflowButton"]'
        self.advancedSearchXpath = '//*[@role = "menu"]'
        self.advancedSearchModalXpath = "//*[@aria-labelledby='modal-header']"
        self.noResultXpath = "//*[contains(text(), 'Não há')]"
        self.noResultXpathEn = "//*[contains(text(), 'No results')]"
        self.explorelink = "https://twitter.com/explore"
        self.likers_xpath = '//*[@data-testid="UserCell"]'
        self.modal_xpath = '//*[@aria-labelledby = "modal-header"]'
        self.user_name_xpath = '//*[@data-testid="UserName"]'
        self.waiting_time = 7200*3
        self.waiting_time_users = 1800
        self.regular_waiting_time = 7200

    def format_date(self, date):
        dateS = date.split('/')
        reformat = dateS[2] + "-" + dateS[1] + "-" + dateS[0]
        return reformat

    def buildSearchString(self, keywords, date):
        searchString = "("

        for keyword in keywords:
            if keywords.index(keyword) == 0:
                searchString = searchString + keyword.lower()
            else:
                searchString = searchString + " OR " + keyword.lower()

        enDate = self.format_date(date)
        searchString = searchString+") lang:pt"+" since:"+enDate
        print(searchString)
        return searchString

    def getUserInfo(self, tweet):
        links = tweet.find_elements_by_tag_name('a')
        tweetBody = tweet.find_element_by_xpath(self.tweetContentXpath).text
        profileLink = links[0].get_attribute('href')
        username = str(links[0].get_attribute('href')).split('/')[-1]

        # retrieve Tweet if not retrieved
        for link in links:
            linkStr = str(link.get_attribute('href'))
            if '/status/' in linkStr:
                tweetId = linkStr.split('/')[-1]
                # print("----Analysing Tweet Id: "+tweetId)
                if not (MongoActions.findTweetById(tweetId)):
                    MongoActions.createTweet(tweetId, tweetBody, username)

    def get_user_link(self, user):
        links = user.find_elements_by_tag_name('a')
        profileLink = links[0].get_attribute('href')
        username = str(links[0].get_attribute('href')).split('/')[-1]
        return [username, profileLink]

    def explore_twitter_using_profile(self, link, isFake = "true"):
        previous_tweets = []
        keep_crawling = True
        height = 400
        times = 0
        login = pl.Login(self.chromeDriver)
        login.doLogin()
        self.chromeDriver.get(link)
        start = time.time()
        
        while keep_crawling:
            tweets = self.get_available_tweets()
            now = time.time()

            if now - start > self.waiting_time:
                keep_crawling = False

            if tweets == None:
                keep_crawling = False

            elif len(tweets) <= 0:
                keep_crawling = False

            elif tweets == previous_tweets:
                times += 1
                height += height
                self.scroll_down(height, self.chromeDriver)
                time.sleep(3)
                if times > 5:
                    keep_crawling = False

            else:
                tweets_list = list(set(tweets)-set(previous_tweets))
                for tweet in tweets_list:
                    links = tweet.find_elements_by_tag_name('a')
                    username = str(links[0].get_attribute('href')).split('/')[-1]
                    profile_link = links[0].get_attribute('href')
                    if(not("retweetou" in tweet.accessible_name) and (username == 'g1' or username == 'JornalOGlobo'  or username == 'cartacapital')):
                        self.get_user_info(profile_link, username)
                        self.get_one_tweet(links, tweet, username, isFake)
                        previous_tweets.clear()
                        previous_tweets.extend(tweets)
                        times = 0
                        
    def explore_twitter_using_quotes(self, quote):
        previous_tweets = []
        keep_crawling = True
        height = 400
        times = 0
        login = pl.Login(self.chromeDriver)
        login.doLogin()
        self.chromeDriver.get(self.explorelink)
        self.wait.waitUntilElementLoads(self.searchFieldXpath, "campo de busca")
        search_field = self.chromeDriver.find_element_by_xpath(self.searchFieldXpath)
        search_field.send_keys(quote)
        search_field.send_keys(Keys.RETURN)
        time.sleep(20)
        start = time.time()

        while keep_crawling:
            tweets = self.get_available_tweets()
            now = time.time()

            if now - start > self.waiting_time:
                keep_crawling = False

            if tweets == None:
                keep_crawling = False

            elif len(tweets) <= 0:
                keep_crawling = False

            elif tweets == previous_tweets:
                times += 1
                height += height
                self.scroll_down(height, self.chromeDriver)
                time.sleep(3)
                if times > 5:
                    keep_crawling = False

            else:
                tweets_list = list(set(tweets)-set(previous_tweets))
                for tweet in tweets_list:
                    links = tweet.find_elements_by_tag_name('a')
                    username = str(links[0].get_attribute('href')).split('/')[-1]
                    profile_link = links[0].get_attribute('href')
                    self.get_user_info(profile_link, username)
                    self.get_one_tweet(links, tweet, username)
                    previous_tweets.clear()
                    previous_tweets.extend(tweets)
                    times = 0

    def record_event(self, tweet_id, username, event_type):
        if not (MongoActions.find_event(tweet_id, username, event_type)):
            MongoActions.create_event(tweet_id, username, event_type)
            return True
        else:
            return False

    def get_likers_sharers(self, tweet_link, tweet_id):
        like_number = 0
        share_number = 0
        likes_driver = DriverHandle.createChromeDriver()
        action = ActionChains(likes_driver)
        login = pl.Login(likes_driver)
        login.doLogin()
        likes_driver.get(tweet_link+"/likes")
        wait = hw.Wait(likes_driver)
        keep_crawling_likers = True
        keep_crawling_sharers = True
        times_likers = 0
        times_sharers = 0
        height = 400
        likers_aux = []
        sharers_aux = []
        wait.waitUntilElementLoads(self.likers_xpath, "likers element")
        time.sleep(3)
        likers = likes_driver.find_elements_by_xpath(self.modal_xpath + self.likers_xpath)
        start_likers = time.time()

        while keep_crawling_likers:
            now_likers = time.time()
            if now_likers - start_likers > self.waiting_time:
                keep_crawling_likers = False
            tries = 0

            if len(likers) <= 0:
                keep_crawling_likers = False

            elif likers_aux == likers:
                try:
                    action.move_to_element(likers[-1]).perform()
                    time.sleep(2)
                    likers = likes_driver.find_elements_by_xpath(self.modal_xpath + self.likers_xpath)
                    times_likers += 1
                except:
                    if tries > 5:
                        raise Exception("Erro ao tentar acessar os elementos de likers")
                    else:
                        likers = likes_driver.find_elements_by_xpath(self.modal_xpath + self.likers_xpath)
                        tries += 1

                if times_likers > 5:
                    keep_crawling_likers = False

            else:
                likers_list = list(set(likers) - set(likers_aux))
                for liker in likers_list:
                    user_info = self.get_user_link(liker)
                    self.get_user_info(user_info[1], user_info[0])
                    if self.record_event(tweet_id, user_info[0], "like"):
                        print("User "+user_info[0]+" liked a fake tweet")
                        self.likes_qtd += 1
                        like_number += 1

                likers_aux.clear()
                likers_aux.extend(likers)
                times_likers = 0


        likes_driver.get(tweet_link + "/retweets")
        wait = hw.Wait(likes_driver)
        wait.waitUntilElementLoads(self.modal_xpath + self.likers_xpath, "sharers element")
        time.sleep(2)
        sharers = likes_driver.find_elements_by_xpath(self.modal_xpath + self.likers_xpath)
        start_sharers = time.time()
        while keep_crawling_sharers:
            now_sharers = time.time()

            if now_sharers - start_sharers > self.waiting_time:
                keep_crawling_sharers = False

            if len(sharers) <= 0:
                keep_crawling_sharers = False

            elif sharers_aux == sharers:
                action.move_to_element(sharers[-1]).perform()
                time.sleep(2)
                sharers = likes_driver.find_elements_by_xpath(self.modal_xpath + self.likers_xpath)
                times_sharers += 1
                if times_sharers > 5:
                    keep_crawling_sharers = False

            else:
                sharers_list = list(set(sharers) - set(sharers_aux))
                for sharer in sharers_list:
                    user_info = self.get_user_link(sharer)
                    self.get_user_info(user_info[1], user_info[0])
                    if self.record_event(tweet_id, user_info[0], "retweet"):
                        self.shares_qtd += 1
                        share_number += 1
                        print("User "+user_info[0]+" shared a fake tweet")
                sharers_aux.clear()
                sharers_aux.extend(sharers)
                times_sharers = 0

        likes_driver.close()
        return {'shares': share_number, 'likes': like_number}


    def scroll_down(self, height, driver):
        height += 200
        driver.execute_script("window.scrollTo(0," + str(height) + ")")
        time.sleep(1)

    def get_available_tweets(self):
        time.sleep(10)
        if self.wait.waitUntilElementLoads(self.teewtsConteinerXpath, "Container de tweets"):
         if self.wait.waitUntilElementLoads("//*[@data-testid='tweet']", "tweets"):
            tweets_conteiner = self.chromeDriver.find_element_by_xpath(self.teewtsConteinerXpath)
            return tweets_conteiner.find_elements_by_xpath("//*[@data-testid='tweet']")
        else:
            return []

    def get_one_tweet(self, tweet_links, tweet, username, isFake = "true"):
        tweetBody = tweet.find_element_by_xpath(self.tweetContentXpath).text
        time = ''
        try:
            time = tweet.find_element_by_tag_name("time").get_attribute('datetime')
        except:
            time = 'notime'
        tweet_id = ''
        for link in tweet_links:
            linkStr = str(link.get_attribute('href'))
            if '/status/' in linkStr:
                tweet_id = linkStr.split('/')[-1]
                # print("----Analysing Tweet Id: "+tweet_id)
                if not (MongoActions.findTweetById(tweet_id)):
                    MongoActions.createTweet(tweet_id, tweetBody, username, time, isFake)
                    return self.get_likers_sharers(linkStr, tweet_id)
    
    def get_one_tweet_body(self, tweet_links, tweet, username):
        body_driver = DriverHandle.createChromeDriver()
        bodyWait = hw.Wait(body_driver)
        right_link = ''
        
        for link in tweet_links:
            current_link = link.get_attribute('href')
            if username+"/status" in current_link:
                right_link = current_link
                break
        
        if right_link == '':
            return
                
        body_driver.get(right_link)
        
        #css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0
        if(bodyWait.waitUntilElementLoads('//*[@class = "css-901oao r-18jsvk2 r-37j5jr r-1blvdjr r-16dba41 r-vrz42v r-bcqeeo r-bnwqim r-qvutc0"]', "Tweet Xpath")):
            tweetBody = body_driver.find_element_by_xpath('//*[@class = "css-901oao r-18jsvk2 r-37j5jr r-1blvdjr r-16dba41 r-vrz42v r-bcqeeo r-bnwqim r-qvutc0"]').text      
            tweet_id = ''
            for link in tweet_links:
                linkStr = str(link.get_attribute('href'))
                if '/status/' in linkStr:
                    tweet_id = linkStr.split('/')[-1]
                    # print("----Analysing Tweet Id: "+tweet_id)
                    MongoActions.create_user_msg(tweetId= tweet_id,tweetBody= tweetBody,username= username)
                    break
                
        body_driver.close()
        
    def get_user_info(self, profile_link, username):
        userDriver = DriverHandle.createChromeDriver()
        userWait = hw.Wait(userDriver)
        userDriver.get(profile_link)
        keep_trying = True
        tries = 0
        description = ''
        joinDate = ''
        location = ''
        followers = ''
        following = ''
        birthdate = ''

        while keep_trying:
            try:
                if userWait.waitUntilElementLoads(self.userDescriptionXpath, "user description", 3):
                    descriptionEle = userDriver.find_element_by_xpath(self.userDescriptionXpath)
                    description = descriptionEle.text
                
                if userWait.waitUntilElementLoads(self.location_xpath, "user location", 3):
                    location_ele = userDriver.find_element_by_xpath(self.location_xpath)
                    location = location_ele.text
                
                if userWait.waitUntilElementLoads(self.user_birthdate_xpath, "user birthdate", 3):
                    birth_ele = userDriver.find_element_by_xpath(self.user_birthdate_xpath)
                    birthdate = birth_ele.text

                if userWait.waitUntilElementLoads(self.userHeadInfoXpath, "user metadata", 3):
                    userProfileItems = userDriver.find_element_by_xpath(self.userHeadInfoXpath)
                    # print("Metadata: " + userProfileItems.text)

                userLinks = userDriver.find_elements_by_tag_name('a')
                for userLink in userLinks:
                    if "followers" in str(userLink.get_attribute('href')):
                        followers = userLink.text
                    elif "following" in str(userLink.get_attribute('href')):
                        following = userLink.text

                if not MongoActions.findUserByName(username):
                    MongoActions.createUser(username, profile_link, description, joinDate, location, following, followers, birthdate)
                    print('User created! Username: ' + username)

                userDriver.quit()
                keep_trying = False

            except:
                if tries > 5:
                    if userDriver:
                        userDriver.quit()
                    keep_trying = False
                else:
                    tries += 1
                    
    def explore_twitter_by_user_link(self, user):
        
        previous_tweets = []
        keep_crawling = True
        height = 400
        times = 0
        login = pl.Login(self.chromeDriver)
        didLogin = login.doLogin()
        
        if didLogin:
            self.chromeDriver.get(user.profileLink)
            if self.wait.waitUntilElementLoads(self.user_name_xpath, "username field"):
                user_name_element = self.chromeDriver.find_element_by_xpath(self.user_name_xpath)
                
                if(user.username in user_name_element.text):
                    print("Extracting tweets from "+user.username)
        
                    start = time.time()
                    while keep_crawling:
                        query =  MongoActions.count_all_user_msg(user.username)
                        tweets = self.get_available_tweets()
                        now = time.time()

                        if now - start > self.waiting_time_users:
                            keep_crawling = False

                        if tweets == None:
                            keep_crawling = False

                        elif len(tweets) <= 0:
                            keep_crawling = False

                        elif tweets == previous_tweets:
                            times += 1
                            height += height
                            self.scroll_down(height, self.chromeDriver)
                            time.sleep(3)
                            if times > 5:
                                keep_crawling = False
                                
                        elif query >= 100:
                            keep_crawling = False
                            
                        else:
                            tweets_list = list(set(tweets)-set(previous_tweets))
                            for tweet in tweets_list:
                                try:
                                    links = tweet.find_elements_by_tag_name('a')
                                    username = str(links[0].get_attribute('href')).split('/')[-1]
                                    if(not("retweetou" in tweet.accessible_name) and username == user.username):
                                        self.get_one_tweet_body(links, tweet, username)
                                    previous_tweets.clear()
                                    previous_tweets.extend(tweets)
                                    times = 0
                                except:
                                    break
            
                else:
                    print(user.username+" not found in twitter! Moving on to other user")
            else:
                print(user.username+" not found in twitter! Moving on to other user")
        else:
            print("Could not login, moving on to next user.")
        