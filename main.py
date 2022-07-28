from Helpers.DriverHandle import DriverHandle
import Pages.Login as pl
import Pages.General as pg
import Pages.Boatos as bt
from selenium.webdriver.common.keys import Keys
import time
import os
from Mongo.MongoActions import MongoActions
from selenium.webdriver.common.action_chains import ActionChains
from mongoengine import connect

connect(host= str(os.environ.get("FAKE")))
# print("Connected in host: "+str(os.environ.get("FAKE")))
# mongoActions = MongoActions()
# mongoActions.generate_user_tweets_dataframe()
# print("Connected in host: "+str(os.environ.get("FAKE")))
profiles = ["https://twitter.com/g1", "https://twitter.com/JornalOGlobo", "https://twitter.com/cartacapital"]
driver = DriverHandle().createChromeDriver()
general = pg.General(driver)


for profile in profiles:
    general.explore_twitter_using_profile(profile, isFake="false")
    


