import os
import time

from urllib3 import Retry
class Login:

    def __init__(self, webdriver):
        self.chromeDriver = webdriver

    def doLogin(self):
       didLogin = False
       times = 0
       while(not(didLogin)):
        try:
            self.chromeDriver.get('https://twitter.com/home')
            #time.sleep(10)
            self.chromeDriver.add_cookie({'name': 'auth_token', 'value': os.environ.get("TWITTERTOKEN"), 'domain': '.twitter.com'})
            self.chromeDriver.get('https://twitter.com/home')
            didLogin = True
            return True
        except:
            if times > 5:
                return False
            else:
                times+=1
                
