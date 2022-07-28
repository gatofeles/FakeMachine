from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Wait:

    def __init__(self, webdriver):
        self.chromeDriver = webdriver
    
    # def waitUntilElementLoads(self, xpath, elementName):
    #
    #     try:
    #         WebDriverWait(self.chromeDriver, 60).until(EC.presence_of_element_located((By.XPATH, xpath)))
    #         return True
    #     except:
    #         print("Elemento "+elementName+" não encontrado.")
    #         return False
    
    def waitUntilElementLoads(self, xpath, elementName, time = 20):
        try:
            WebDriverWait(self.chromeDriver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except:
            print("Elemento "+elementName+" não encontrado.")
            return False


        

