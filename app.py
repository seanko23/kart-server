from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

class MapRecords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), nullable=False)
	password = db.Column(db.String(20), nullable=False)
	ign = db.Column(db.String(15), nullable=False, default='N/A')
	map1 = db.Column(db.String(7), nullable=False, default='N/A')
	map2 = db.Column(db.String(7), nullable=False, default='N/A')
	map3 = db.Column(db.String(7), nullable=False, default='N/A')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return 'User id:' + str(self.id) +' and user ign: ' + self.ign

@app.route('/')
def index():
	# will have the ability to either login or look up an IGN
	return render_template("index.html")


@app.route('/signin', methods=['POST', 'GET']) #enable sign up
def signin():
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		#existing_username = MapRecords.query.
		#query
		#exisitng_password = #query

	return render_template("/signin.html")


@app.route('/visitor')
def visitor():
	return render_template("visitor.html")

@app.route('/signin/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		post_confirm_password = request.form['confirm_password']
		if post_password == post_confirm_password:
			new_user = MapRecords(username=post_username, password=post_password)
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