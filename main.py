import requests
from bs4 import BeautifulSoup 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

URL = 'https://support.industry.siemens.com/forum/WW/en/topics/#!?&OnlyNewTopics=false&SortOrder=lastpost_desc&TopicsByUserName='

driver.get(URL)