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
url = 'https://reach.vic.gov.au/#/vccaw/icu'
driver.get(url)
time.sleep(10) #needed for site generation time
soup = BeautifulSoup(driver.page_source, features="html.parser").find(id="dashboardtable")
hospitals = soup.find_all('tr', attrs={"data-row-name": "CampusBedNumbers"})

bedstate = []

for hospital in hospitals:
	cells = hospital.find_all("td")
	if cells[0].parent['class'][0] == "care-Tertiary":
		tertiary, metro, public = 1, 1, 1
	elif cells[0].parent['class'][0] == "care-SubTertiary":
		tertiary, metro, public = 0, 1, 1
	elif cells[0].parent['class'][0] == "care-Regional":
		tertiary, metro, public = 0, 0, 1
	elif cells[0].parent['class'][0] == "care-Private":
		tertiary, metro, public = 0, 0, 0
	hospital_state = {
		"name": cells[0].find("span").get_text(),
		"tertiary": tertiary,
		"metro": metro,
		"public": public,
		"icu_empty": cells[1].find("span").get_text(),
		"icu_occupied": cells[2].find("span").get_text(),
		"icu_await_admit": cells[3].find("span").get_text(),
		"icu_await_dc": cells[4].find("span").get_text(),
		"hdu_empty": cells[5].find("span").get_text(),
		"hdu_occupied": cells[6].find("span").get_text(),
		"hdu_await_admit": cells[7].find("span").get_text(),
		"hdu_await_discharge": cells[8].find("span").get_text(),
		"hdu_min_icu_equiv": cells[9].find("span").get_text(),
		"updated": cells[10].find("span").get("data-tooltip")
	}
	bedstate.append(hospital_state)

with open('bedstate.json', 'w') as outfile:
	json.dump(bedstate, outfile)


##Victorian COVID-19
url = 'https://reach.vic.gov.au/#/hird/home'
driver.get(url)
time.sleep(10) #needed for site generation time
soup = BeautifulSoup(driver.page_source, features="html.parser").find(id="dashboardtable")
hospitals = soup.find_all('tr', attrs={"data-row-name": "CampusBedNumbers"})

#Housekeeping
driver.quit()