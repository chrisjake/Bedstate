import time #for rendering delay
from datetime import datetime #for timestamping
import json #for dumping results ?delete with working psql
import sql_functions #local set of instructions for updating PSQL DB
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import psycopg2
import sqlconfig #psql settings file


chrome_options = Options()
chrome_options.add_argument("--headless") #comment out for debugging
driver = webdriver.Chrome(options=chrome_options)

dtg = datetime.utcnow()

#ICU Occupancy Data
##Victorian Bedstate
url = 'https://reach.vic.gov.au/#/vccaw/icu'
driver.get(url)
time.sleep(15) #needed for site generation time
soup = BeautifulSoup(driver.page_source, features="html.parser").find(id="dashboardtable")
hospitals = soup.find_all('tr', attrs={"data-row-name": "CampusBedNumbers"})

bedstate = []
hospital_static = []


###Static Values
def vic_static():
	for hospital in hospitals:
		cells = hospital.find_all("td")
		if cells[0].parent['class'][0] == "care-Tertiary":
			tertiary, metro, private = 1, 1, 0
		elif cells[0].parent['class'][0] == "care-SubTertiary":
			tertiary, metro, private = 0, 1, 0
		elif cells[0].parent['class'][0] == "care-Regional":
			tertiary, metro, private = 0, 0, 0
		elif cells[0].parent['class'][0] == "care-Private":
			tertiary, metro, private = 0, 0, 1
		hospital_state = {
			"title": cells[0].find("span").get_text(),
			"tertiary": tertiary,
			"metro": metro,
			"private": private,
			"area": "vic",
		}
		hospital_static.append(hospital_state)
	with open('hospital_static.json', 'w') as outfile:
		json.dump(hospital_static, outfile)


###Dynamic Values
def vic_dynamic():
	conn = None
	try:
		conn = psycopg2.connect(host=sqlconfig.host,database=sqlconfig.database, user=sqlconfig.username, password=sqlconfig.password)
		cur=conn.cursor()
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')
		db_version = cur.fetchone()
		print(db_version)
		return conn
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	cur = conn.cursor()
	for hospital in hospitals:
		cells = hospital.find_all("td")
		hospital_state = {
			"title": cells[0].find("span").get_text(),
			"icu_emp": cells[1].find("span").get_text(),
			"icu_occ": cells[2].find("span").get_text(),
			"icu_aw_adm": cells[3].find("span").get_text(),
			"icu_aw_dc": cells[4].find("span").get_text(),
			"hdu_emp": cells[5].find("span").get_text(),
			"hdu_occ": cells[6].find("span").get_text(),
			"hdu_aw_adm": cells[7].find("span").get_text(),
			"hdu_aw_dc": cells[8].find("span").get_text(),
			"min_icu_eqv": cells[9].find("span").get_text(),
			"updated": cells[10].find("span").get("data-tooltip"),
			"ts": str(dtg)
		}
		print(hospital_state)
		columns = hospital_state.keys() #
		values = [hospital_state[column] for column in columns]
		sql = "insert into bedstate (%s) values %s"
		cur.execute(sql, (AsIs(','.join(columns)), tuple(values)))

		with open('hospitalstate.json', 'w') as outfile: #debugging with json output
			json.dump(hospital_state, outfile)
		bedstate.append(hospital_state)

	with open('bedstate.json', 'w') as outfile:
		json.dump(bedstate, outfile)

vic_dynamic()




##Upload to Database


##Victorian COVID-19
url = 'https://reach.vic.gov.au/#/hird/home'
driver.get(url)
time.sleep(10) #needed for site generation time
soup = BeautifulSoup(driver.page_source, features="html.parser").find(id="dashboardtable")
hospitals = soup.find_all('tr', attrs={"data-row-name": "CampusBedNumbers"})

#Housekeeping
driver.quit()