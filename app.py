from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

	

@app.route('/')
def index():
	# will have the ability to either login or look up an IGN
	return render_template("index.html")


@app.route('/signin', methods=['POST', 'GET']) #enable sign up
def signin():
	from model import User, MapRecords
	if request.method == 'POST':
		conn = sqlite3.connect('records.db')
		cur = conn.cursor()    
		cur.execute('SELECT username, password FROM user')
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
	from model import User, MapRecords
	if request.method == 'POST':
		pass

	return render_template("account.html")


@app.route('/signin/account/chart')
def graph():
	return render_template('chart.html')

@app.route('/signin/account/records/', methods=['POST', 'GET'])
def records():
	from model import User, MapRecords
	if request.method == 'POST':
		print('HELLO')
		post_ign = request.form['user_ign']
		post_map1 = request.form['map1_record']
		post_map2 = request.form['map2_record']
		post_map3 = request.form['map3_record']
		post_map4 = request.form['map4_record']
		post_map5 = request.form['map5_record']
		post_map6 = request.form['map6_record']
		post_map7 = request.form['map7_record']
		post_map8 = request.form['map8_record']
		user = User.query.filter_by(ign=post_ign).first()
		new_records = MapRecords(user=user, map1=post_map1, map2=post_map2, map3=post_map3, map4=post_map4, map5=post_map5, map6=post_map6, map7=post_map7, map8=post_map8)
		cur_db = db.session.object_session(new_records)
		cur_db.add(new_records)
		cur_db.commit()
		# db.session.add(new_records)
		# db.session.commit()
		return redirect('/signin')

	return render_template('records.html')


@app.route('/visitor')
def visitor():
	return render_template("visitor.html")


@app.route('/signin/signup/', methods=['POST', 'GET'])
def signup():
	from model import User
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		post_confirm_password = request.form['confirm_password']
		if post_password == post_confirm_password:
			new_user = User(username=post_username, password=post_password)
			db.session.add(new_user)
			db.session.commit()
			return redirect('/signin')
		elif post_password != post_confirm_password:
			pass_list=[post_password,post_confirm_password]
			return render_template('signup.html', pass_list=pass_list)
	else:
		return render_template('signup.html')


if __name__ == '__main__':
	app.run(debug=True)
