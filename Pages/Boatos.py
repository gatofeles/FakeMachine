from Helpers.DriverHandle import DriverHandle
from Helpers.Wait import Wait
import re
from Pages import General as gen
from Mongo.MongoActions import MongoActions
import time
import sys
class Boatos:
    def __init__(self):
        self.tweetRegex = '/^https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)$/'
        self.webdriver = DriverHandle.createChromeDriver()
        self.linkTweetSearch = 'https://www.boatos.org/?s=tweet&fromt=yes'
        self.articleXpath = '//*[@class="entry-content clearfix"]'
        self.wait = Wait(self.webdriver)
        self.categoryContentXpath ='//*[@id = "primary"]'
        self.quotes_xpath = '//*[@id = "primary"]//p//span[@style ="color: #ff0000;"]'
        self.newsContextXpath = '//*[@class="entry-content clearfix"]'
        self.dateXpath = '//*[@class="entry-date published"]'
        self.categoryContent = None
        self.categoryContents = None

    def get_available_checks(self):
  
        self.webdriver.get(self.linkTweetSearch)
        self.wait.waitUntilElementLoads(self.categoryContentXpath, 'category content')
        self.categoryContent = self.webdriver.find_element_by_xpath(self.categoryContentXpath)
        self.categoryContents = self.categoryContent.find_elements_by_tag_name("article")
            
    def split_phrase(self, regex, phrase):
        tweets = re.compile(regex).split(phrase)
        for tweet in tweets:
            tweet.strip()
        return tweets[1:]

    def get_tweet_directly(self, checked_tweet):
        links = checked_tweet.find_elements_by_tag_name('a')
        for link in links:
            if re.match(self.tweetRegex, link.get_attribute('href')):
                direct_tweet_driver = DriverHandle.createChromeDriver()
                general = gen.General(direct_tweet_driver)

    def get_tweet_from_quotes(self, checked_tweet):
        mongo_actions = MongoActions()
        link_element = checked_tweet.find_elements_by_tag_name('a')
        link = link_element[2].get_attribute('href')
        content_driver = DriverHandle.createChromeDriver()
        content_driver.get(link)
        print("On Boatos Page")
        content_wait = Wait(content_driver)

        if content_wait.waitUntilElementLoads(self.quotes_xpath, 'quotes Xpath'):
            quotes = content_driver.find_elements_by_xpath(self.quotes_xpath)
            print("On Quotes Extraction")
            for quote in quotes:
                quote_text = quote.text
                if not(mongo_actions.find_head_by_quote(quote_text)):
                    mongo_actions.register_header(quote_text)
                    twitter_driver = DriverHandle.createChromeDriver()
                    general = gen.General(twitter_driver)
                    print("On Twitter")
                    general.explore_twitter_using_quotes(quote_text)
                    twitter_driver.close()

        content_driver.close()

    def get_tweet_from_header(self, checked_tweet):
        content_body = checked_tweet
        content = content_body.find_element_by_tag_name('p')
        date = content_body.find_element_by_tag_name('time')

        # Visitar página seguinte e pegar texto
        link_element = checked_tweet.find_elements_by_tag_name('a')
        link = link_element[2].get_attribute('href')
        content_driver = DriverHandle.createChromeDriver()
        content_driver.get(link)
        tweet_string = content_driver.find_element_by_tag_name('strong').text
        content_driver.close()

        # contentText = content.text
        date_text = date.text
        twitter_driver = DriverHandle.createChromeDriver()
        general = gen.General(twitter_driver)
        general.exploreTwitter(tweet_string.split("Boato")[1], date_text)
        twitter_driver.close()

    def get_tweets(self):
        self.get_available_checks()
        for check in self.categoryContents:
            self.get_tweet_from_header(check)

    def get_tweets_from_quotes(self):
        self.get_available_checks()
        print("quantidade de chamadas: "+ str(len(self.categoryContents)))
        print("texto de chamada teste: " + self.categoryContents[0].text)
        for check in self.categoryContents:
            self.get_tweet_from_quotes(check)

    



