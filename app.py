import psycopg2
from flask import Flask
from flask import request, send_from_directory
import json
from neo4j.v1 import GraphDatabase, basic_auth
import pandas as pd
import networkx as nx
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
	return send_transactions(source,target)

@app.route('/amount')
def amount():
	print('entered')
	source = request.args.get('first_client')
	target = request.args.get('second_client')
	value = request.args.get('transaction_count')
	return send_total_transactions(source,target)



def connect():
	connect_str = "dbname='lauzhack' user='lauzhack' host='165.227.134.175' password='lauzhack2017'"
	# use our connection values to establish a connection
	conn = psycopg2.connect(connect_str)
	return conn

def ne04j_new_session():
	driver = GraphDatabase.driver("bolt://165.227.134.175", auth=basic_auth("user", "lauzhack2017"))
	return driver.session()

def get_total_transaction(source,target):
	transactions = pd.read_csv('./sample_data/transactions.small.csv')
	df = transactions.groupby(['source', 'target'])['amount'].sum()
	return df

def get_transaction(source,target):
	transactions = pd.read_csv('./sample_data/transactions.small.csv')
	df = transactions[transactions['source']==source]
	df = df[df['target']==target]
	df = df[['source','target','amount']]
	return transactions

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


def find_cycle(source, transactions):
	edges = transactions[['source', 'target', 'amount']]
	directedGraph = nx.from_pandas_dataframe(edges,source='source',
                                   target='target', edge_attr='amount', create_using=nx.DiGraph())
	cycle = nx.find_cycle(directedGraph, source, 'original' )
	return cycle

def send_total_transactions(source,target):
	tt = get_total_transaction(source,target)
	tt['date']='2015'
	tt['time']='none'
	tt['currency']= None
	tt['group'] = 0
	arr = tt.to_dict()
	json_string = json.dumps(arr)
	return json_string
	
def send_transactions(source,target):
	transactions = get_transaction(source,target)
	transactions['group']=1
	transactions = transactions.head(600)
	df1 = transactions
	cycle_init = 'a009461d-6293-4010-ac28-7f5aeb83bd82'
	cycle = find_cycle(cycle_init, transactions)
	labels = ['source', 'target']
	df = pd.DataFrame.from_records(cycle, columns=labels)

	df2 = transactions[transactions['source'].isin(df['source'].values) & transactions['target'].isin(df['target'].values)]

	df1['group'] = pd.Series(df1.index).apply(lambda x: 1 if x in df2.index.values else 4)
	

	arr = df1.to_dict('records')
	json_string = json.dumps(arr)
	return json_string


	

if __name__ == '__main__':
    app.run()
