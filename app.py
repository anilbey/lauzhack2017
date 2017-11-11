import psycopg2
from flask import Flask
import json
app = Flask(__name__)




@app.route('/atms')
def atms():
	try:
		conn = connect()
		# create a psycopg2 cursor that can execute queries
		cursor = conn.cursor()
		# create a new table with a single column called "name"
		#cursor.execute("""CREATE TABLE tutorials (name char(40));""")
		# run a SELECT statement - no data in there, but we can try it
		cursor.execute("""SELECT * from atms""")
		rows = cursor.fetchall()
		return json.dumps(rows)
	except Exception as e:
		print("Uh oh, can't connect. Invalid dbname, user or password?")
		print(e)
	return e


def connect():
	connect_str = "dbname='lauzhack' user='lauzhack' host='165.227.134.175' password='lauzhack2017'"
	# use our connection values to establish a connection
	conn = psycopg2.connect(connect_str)
	return conn


if __name__ == '__main__':
    app.run()
