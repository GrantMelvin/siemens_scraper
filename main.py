import requests
from bs4 import BeautifulSoup 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

URL = 'https://support.industry.siemens.com/forum/WW/en/topics/#!?&OnlyNewTopics=false&SortOrder=lastpost_desc&TopicsByUserName='

driver.get(URL)

# Optionally, wait for the "Accept All Cookies" button to be clickable
try:
    time.sleep(5)
    # Adjust the By selector and the class name as per the actual website's button
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']"))
    )
    
    # Simulate a click action on the "Accept All Cookies" button
    accept_button.click()

except Exception as e:
    print(f"An error occurred: {e}")
