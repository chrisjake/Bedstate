import sqlconfig #psql settings file
import psycopg2 #psqldumping
from psycopg2.extensions import AsIs

def connect():
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


def disconnect():
	conn.close()
	print('Database connection closed.')



def create_tables():
	try:
		conn
		print("Already connected")
	except NameError:
		conn = connect()
		print("Now connected")
	commands = (
		"""
		CREATE TABLE hospitals (
			id serial NOT NULL PRIMARY KEY,
			title varchar,
			metro bool,
			private bool,
			tertiary bool,
			area char(3)
		);
		""",
		"""
		CREATE TABLE bedstate (
			id serial NOT NULL PRIMARY KEY,
			title varchar,
			icu_occ smallint,
			icu_emp smallint,
			icu_aw_adm smallint,
			icu_aw_dc smallint,
			hdu_occ smallint,
			hdu_emp smallint,
			hdu_aw_adm smallint,
			hdu_aw_dc smallint,
			min_icu_eqv smallint,
			updated varchar,
			ts timestamptz
		);
		"""
		)
	cur = conn.cursor()
	for command in commands:
		cur.execute(command)
	cur.close()
	conn.commit()
	print('Tables created.')
	return conn


#def insert_values():
#	conn = connect()
#	columns = hospital_state.keys()
#	values = [hospital_state[column] for column in columns]] 
#
#	sql = "insert into bedstate (%s) values %s"
#	cursor.execute(sql, (AsIs(','.join(columns)), tuple(values)))
	

#	str(INSERT INTO bedstate (title, icu_occ, icu_emp, icu_aw_adm, icu_aw_dc, hdu_occ, hdu_emp, hdu_aw_adm, hdu_aw_dc, min_icu_eqv, updated, ts)
#		VALUES(cells[0].find("span").get_text(), cells[2].find("span").get_text(), cells[1].find("span").get_text(), cells[3].find("span").get_text(), cells[4].find("span").get_text(), cells[6].find("span").get_text(), cells[5].find("span").get_text(), cells[7].find("span").get_text(), cells[8].find("span").get_text(), cells[9].find("span").get_text(), cells[10].find("span").get("data-tooltip"), str(dtg));
#		)
#	cur=con.cursor()#	disconnect(conn)


#create_tables()
#disconnect()

#connect()