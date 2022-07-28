from sre_constants import SUCCESS
from Helpers.DriverHandle import DriverHandle
import Pages.Login as pl
import Pages.General as pg
import Pages.Boatos as bt
from selenium.webdriver.common.keys import Keys
from Mongo.MongoActions import MongoActions
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from mongoengine import connect

connect(host= str(os.environ.get("FAKE")))

users = MongoActions.get_all_users()
webdriver = DriverHandle.createChromeDriver()
general = pg.General(webdriver)

for user in users:
    general.explore_twitter_by_user_link(user)
