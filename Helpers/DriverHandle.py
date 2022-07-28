from selenium import webdriver
import os
import time

class DriverHandle:

    def createChromeDriver(runHeadless = False, type = "boatos_main", local_run = False):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        #chrome_options.add_argument('--headless')
        times = 0
        keep_trying = True
        time.sleep(2)
        
        if not(local_run):
            if type == "boatos_main":
                url = "http://172.18.0.3:5555/wd/hub"
            elif type == "boatos_quote":
                url = "http://172.18.0.3:5555/wd/hub"

            while keep_trying:
                try:
                    driver = webdriver.Remote(
                        command_executor="http://172.18.0.3:5555/wd/hub",
                        options=chrome_options
                    )
                    keep_trying = False
                except:
                    if times > 10:
                        raise Exception("Unable to connect to the grid")
                    else:
                        times += 1
                        time.sleep(1)
            return driver
        
        else:
            driver = webdriver.Chrome('C:\\Users\\alexo\source\\repos\\scrapingTwitter\\driver\\chromedriver.exe')          
            return driver


