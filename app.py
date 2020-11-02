from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# TODO: encapsulate this code to create_app and call this from ifname
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

	

@app.route('/')
def index():
	# will have the ability to either login or look up an IGN
	return render_template("index.html")


@app.route('/signin', methods=['POST', 'GET']) #enable sign up
def signin():
	from model import Users, MapRecords
	if request.method == 'POST':
		conn = sqlite3.connect('records.db')
		cur = conn.cursor()    
		cur.execute('SELECT username, password FROM users')
		user_raw = cur.fetchall()
		global post_username
		post_username = request.form['username']
		post_password = request.form['password']
		counter = 0
		for user in user_raw:
			if user[0] == post_username and user[1] == post_password:
				return redirect(url_for('account'))
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
	from model import Users, MapRecords
	if request.method == 'POST':
		pass

	return render_template("account.html")


@app.route('/signin/account/chart')
def graph():
	return render_template('chart.html')

@app.route('/signin/account/records/', methods=['POST', 'GET'])
def records():
	from model import Users, MapRecords
	if request.method == 'POST':
		# post_ign = request.form['user_ign']
		# post_map1 = request.form['map1_record']
		# post_map2 = request.form['map2_record']
		# post_map3 = request.form['map3_record']
		# post_map4 = request.form['map4_record']
		# post_map5 = request.form['map5_record']
		# post_map6 = request.form['map6_record']
		# post_map7 = request.form['map7_record']
		# post_map8 = request.form['map8_record']
		# user = Users.query.filter_by(ign=post_ign).first()
		# new_records = MapRecords(users=user, map1=post_map1, map2=post_map2, map3=post_map3, map4=post_map4, map5=post_map5, map6=post_map6, map7=post_map7, map8=post_map8)
		# cur_db = db.session.object_session(new_records)
		# cur_db.add(new_records)
		# cur_db.commit()
		# db.session.add(new_records)
		# db.session.commit()
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
		from model import post_maps
		post_maps(post_data)

		return redirect('/signin')

	return render_template('records.html')


@app.route('/visitor')
def visitor():
	return render_template("visitor.html")


@app.route('/signin/signup/', methods=['POST', 'GET'])
def signup():
	from model import Users
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		post_confirm_password = request.form['confirm_password']
		if post_password == post_confirm_password:
			from model import Users
			new_user = Users(username=post_username, password=post_password)
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
@app.route('/maps', methods=['POST'])
def maps():
	from model import post_maps
	
	if request.method == 'POST':
		post_maps(request.get_json())

		response = Response({})
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response

if __name__ == '__main__':
	app.run(debug=True)
