#Not confirmed working as https://reach.vic.gov.au/#/hird/home not yet functional

import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless") #comment out for debugging
driver = webdriver.Chrome(options=chrome_options)


#ICU Occupancy Data
##Victorian Bedstate

##Victorian COVID-19
url = 'https://reach.vic.gov.au/#/hird/home'
driver.get(url)
time.sleep(10) #needed for site generation time
soup = BeautifulSoup(driver.page_source, features="html.parser").find(id="patientDataTab").find(id="dashboardtable")

hospitals = soup.find_all('tr', attrs={"data-row-name": "CampusBedNumbers"})


#Housekeeping
driver.quit()