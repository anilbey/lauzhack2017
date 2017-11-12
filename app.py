import psycopg2
from flask import Flask
from flask import request, send_from_directory
import json
from neo4j.v1 import GraphDatabase, basic_auth
import pandas as pd
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
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('static', path)

@app.route('/search')
def search():
	print('entered')
	source = request.args.get('first_client')
	target = request.args.get('second_client')
	value = request.args.get('transaction_count')
	print(source+target+value)
	return get_transaction(source,target)

def connect():
	connect_str = "dbname='lauzhack' user='lauzhack' host='165.227.134.175' password='lauzhack2017'"
	# use our connection values to establish a connection
	conn = psycopg2.connect(connect_str)
	return conn

def ne04j_new_session():
	driver = GraphDatabase.driver("bolt://165.227.134.175", auth=basic_auth("user", "lauzhack2017"))
	return driver.session()

def get_transaction(source,target):
	transactions = pd.read_csv('./sample_data/transactions.small.csv')
	df = transactions[transactions['source']==source]
	df = df[df['target']==target]
	df = df[['source','target','amount']]


	gb = transactions.groupby(['source', 'target'])
	counts = gb.size().to_frame(name='counts')
	view1 = (counts .join(gb.agg({'amount': 'mean'}).rename(columns={'amount': 'amount_mean'}))
	.join(gb.agg({'amount': 'median'}).rename(columns={'amount': 'amount_median'}))
	.join(gb.agg({'amount': 'sum'}).rename(columns={'amount': 'amount_sum'}))
	 .reset_index()
	)

	view1 = view1[['source','target','amount_sum']]
	df = view1[view1['source']==source]
	df = df[df['target']==target]
	df = df[['source','target','amount_sum']]
	print('sss')

	transactions['group']=1
	arr = transactions.head(20).to_dict('records')
	json_string = json.dumps(arr)
	return json_string

if __name__ == '__main__':
    app.run()
