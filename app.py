from flask import (
	Flask,
	render_template,
	request,
	redirect,
	url_for,
	Response,
	json,
)
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn import preprocessing
from database import (
	db,
	Users,
	MapRecords,
	post_maps,
	get_maps_by_users,
	get_maps_by_map,
)
import sqlite3



def create_app():
	app = Flask(__name__)
	app.config['DEBUG'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
	db.init_app(app)
	CORS(app)
	return app

	
app = create_app()
@app.route('/')
def index():
	# will have the ability to either login or look up an IGN
	return render_template("index.html")


@app.route('/signin', methods=['POST', 'GET']) #enable sign up
def signin():
	if request.method == 'POST':
		conn = sqlite3.connect('records.db')
		cur = conn.cursor()    
		cur.execute('SELECT username, password, ign FROM users')
		user_raw = cur.fetchall()
		global post_username
		post_username = request.form['username']
		post_password = request.form['password']
		counter = 0
		for user in user_raw:
			if user[0] == post_username and user[1] == post_password:
				return render_template('account.html', name=user[2])
			else:
				counter+=1
				if counter == len(user_raw):
					return render_template('signin.html')
					# have to print out that "Incorrect username/password"
				else:
					pass

	return render_template("signin.html")

@app.route('/signin/account/', methods=['POST', 'GET'])
def account():
	if request.method == 'POST':
		pass

	return render_template("account.html")


@app.route('/signin/account/chart')
def graph():
	return render_template('chart.html')

@app.route('/signin/account/records/', methods=['POST', 'GET'])
def records():
	if request.method == 'POST':
		post_data = {
			'ign': request.form['user_ign'],
			'maps': {
				'빌리지 고가의 질주': request.form['map1_record'],
				'WKC 코리아 서킷': request.form['map2_record'],
				'사막 빙글빙글 공사장': request.form['map3_record'],
				'대저택 은밀한 지하실': request.form['map4_record'],
				'노르테유 익스프레스': request.form['map5_record'],
				'빌리지 운명의 다리': request.form['map6_record'],
				'해적 로비 절벽의 전투': request.form['map7_record'],
				'쥐라기 공룡 결투장': request.form['map8_record']
			}
		}
		post_maps(post_data)

		return render_template("account.html")

	return render_template('records.html')


@app.route('/visitor')
def visitor():
	return render_template("visitor.html")


@app.route('/signin/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		post_username = request.form['username']
		post_ign = request.form['ign']
		post_password = request.form['password']
		post_confirm_password = request.form['confirm_password']
		if post_password == post_confirm_password:
			# TODO: Need to check if username exists already
			new_user = Users(username=post_username, password=post_password, ign=post_ign)
			db.session.add(new_user)
			db.session.commit()
			return redirect('/signin')
		elif post_password != post_confirm_password:
			pass_list=[post_password,post_confirm_password]
			return render_template('signup.html', pass_list=pass_list)
	else:
		return render_template('signup.html')

# POST: accepts map data and puts it in the db. Returns error if input is invalid
# Ex.
# {
# 	ign: `세야`
# 	maps: {
# 		`빌리지 고가의 질주`: '1:45:50',
# 		...
# 	}
# }
# GET: returns map records given 0 or more igns requested
@app.route('/maps', methods=['GET', 'POST'])
def maps():
	
	if request.method == 'POST':
		post_maps(request.get_json())

		response = Response({})
		return response
	else:
		filters = {}
		
		igns = request.args.get('igns')
		map_name = request.args.get('map')
		if igns:
			filters['igns'] = igns.split(',')
			map_records = get_maps_by_users(filters)
		elif map_name:
			map_records = get_maps_by_map(map_name)
		else:
			map_records = get_maps_by_users(filters)
		response = app.response_class(
			response=json.dumps(map_records),
			status=200,
			mimetype='application/json'
		)
		
		return response

@app.route('/chart', methods=['GET', 'POST'])
def chart():
	conn = sqlite3.connect('records.db')

	df = pd.read_sql_query('SELECT ign, map1, map2, map3, map4, map5, map6, map7, map8 FROM map_records INNER JOIN users ON map_records.users_id = users.id', conn)
	print(df)
	sorter = len(df.iloc[:,1:-1].columns)+2
	for i in list(df):
		if i[:3] == 'map':
			df[i] = df[i].astype(float)

	for i in df.iloc[:,2:-7]:
		scaled_values = (-(df[i] - df[i].max())/(df[i].max() - df[i].min()))
		new_column_name = 'scaled_' + i
		df[new_column_name] = scaled_values



	sum_of_records_list = []
	for i in df.iterrows():
		sum_of_records = 0
		for j in i[1][1:sorter-1]:
			sum_of_records+=j
		sum_of_records_list.append(sum_of_records)
		
	mean_value = np.mean(sum_of_records_list)

	for i in range(len(sum_of_records_list)):
		sum_of_records_list[i] = mean_value - sum_of_records_list[i]    

	df['Record_Sum'] = sum_of_records_list

	normalized_values = preprocessing.scale(df['Record_Sum'])

	df['elo'] = normalized_values*100 + 4000
	new_df = df.sort_values(by=['elo']).reset_index(drop=True)
	ranking_df = new_df[['ign','elo']].iloc[::-1].reset_index(drop=True)
	ranking_df['elo'] = round(ranking_df['elo'],0).astype(int)

	ranking_list = [i+1 for i in range(len(ranking_df))]
	ranking_df['rank'] = ranking_list

	cols = ranking_df.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	final_ranking_df=ranking_df[cols]

	final_ranking_df_dict = final_ranking_df.to_dict('records')
	
	print(final_ranking_df_dict)

	response = app.response_class(
		response=json.dumps(final_ranking_df_dict),
		status=200,
		mimetype='application/json'
	)
	return response



if __name__ == '__main__':
	app.run()