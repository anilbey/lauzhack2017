import psycopg2
from flask import Flask
from flask import request, send_from_directory
import json
app = Flask(__name__ , static_url_path='')


@app.route('/')
def root():
	return "obama"

@app.route('/atms')
def atms():
	try:
		conn = connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * from atms")
		rows = cursor.fetchall()
		return json.dumps(rows)
	except Exception as e:
		print(e)
	return e

# to serve static files
@app.route('/sample_data/<path:path>')
def serve_file(path):
    return send_from_directory('sample_data', path)

def connect():
	connect_str = "dbname='lauzhack' user='lauzhack' host='165.227.134.175' password='lauzhack2017'"
	# use our connection values to establish a connection
	conn = psycopg2.connect(connect_str)
	return conn




if __name__ == '__main__':
    app.run()
