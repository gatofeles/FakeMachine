import time
from mongoengine import connect
import os
connect(host= str(os.environ.get("FAKE")))
from behave import *
from Pages.Login import Login
from Pages.General import General
from Helpers.DriverHandle import DriverHandle
from Helpers.Wait import Wait
from selenium.webdriver.common.keys import Keys

@given('I have logged in twitter')
def step_impl(context):
    tries = 0
    keep_trying = True
    test_driver = DriverHandle.createChromeDriver()
    login = Login(test_driver)
    wait = Wait(test_driver)
    login.doLogin()
    while keep_trying:
        try:
            wait.waitUntilElementLoads('//*[@aria-label="Twitter"]', 'label', 20)
            keep_trying = False
        except:
            if tries > 5:
                keep_trying = False
                raise Exception('Could not login')
            else:
                tries += 1
                time.sleep(1)
    context.driver = test_driver
    context.wait = wait

@given('I know how much tweets, likes and shares related to the search "{text}" there is')
def step_impl(context, text):
    explorelink = "https://twitter.com/explore"
    searchFieldXpath = '//*[@data-testid="SearchBox_Search_Input"]'
    context.driver.get(explorelink)

    context.wait.waitUntilElementLoads(searchFieldXpath, "campo de busca")
    searchField = context.driver.find_element_by_xpath(searchFieldXpath)
    searchField.send_keys(text)
    searchField.send_keys(Keys.RETURN)

    teewtsConteinerXpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div'
    context.wait.waitUntilElementLoads(teewtsConteinerXpath, "Container de tweets", 10)
    context.wait.waitUntilElementLoads("//*[@data-testid='tweet']", "tweets", 10)

    tweets_conteiner = context.driver.find_element_by_xpath(teewtsConteinerXpath)
    tweets = tweets_conteiner.find_elements_by_xpath("//*[@data-testid='tweet']")
    context.tweets = tweets
    context.tweet_body = text


@when('I scrap the tweet')
def step_impl(context):
    general = General(context.driver)
    context.wait.waitUntilElementLoads("//*[@data-testid='tweet']", 'tweet', 10)
    tweet = context.driver.find_element_by_xpath("//*[@data-testid='tweet']")
    context.wait.waitUntilElementLoads("//*[@data-testid='app-text-transition-container']", 'likes conteiner', 10)
    like_retweets = tweet.find_elements_by_xpath("//*[@data-testid='app-text-transition-container']")
    like_number = int(like_retweets[1].text)
    share_number = int(like_retweets[2].text)
    links = tweet.find_elements_by_tag_name('a')
    username = str(links[0].get_attribute('href')).split('/')[-1]
    profile_link = links[0].get_attribute('href')
    general.get_user_info(profile_link, username)
    sharers_likers = general.get_one_tweet(links, tweet, username)
    context.like_number = like_number
    context.share_number = share_number
    context.shares_likers = sharers_likers


@then('I should get all likers and sharers of the tweet')
def step_impl(context):
    assert context.like_number == context.sharers_likers['likes'], 'numbers of likes dont match'
    assert context.share_number == context.sharers_likers['shares'], 'numbers of likes dont match'
