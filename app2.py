from flask import (
	Flask,
	render_template,
	request,
	redirect,
	url_for,
	Response,
	json,
	jsonify
)
from flask_cors import CORS
from flask_migrate import Migrate
# import pandas as pd
# import numpy as np
# import math
# from sklearn import preprocessing
from database import (
	db,
	Users,
	MapRecords,
	post_maps,
	get_maps_by_users,
	get_maps_by_map,
	get_elo,
	get_user_info,
	post_sign_in,
	post_sign_up,
)
from maps import (
	get_level_map_dict,
	get_map_name_minimum_dict,
)
import app_constants
import util.util as util
import jwt
#from functools import wraps

from datetime import (datetime, timedelta)

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#When trying to access protected URL with JWT:
# $ export JWT="access_token(actual token)"
# $ http GET :5000/protected Authorization:"Bearer $JWT" -> returns json file
# $ export REFRESH_TOKEN="refresh_token(actual refresh token)"
# $ http POST :5000/refresh Authorization:"Bearer $REFRESH_TOKEN"


def create_app():
	app = Flask(__name__)
	app.config['DEBUG'] = True
	app.config['JWT_SECRET_KEY'] = 'e1a16c7320b6b57d7088ba8c6c3d123efc91f82bb8f5e4ee' # import os -> os.urandom(24).hex()
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10) #timedelta(hours=1)
	app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=20) #timedelta(days=30)
	#app.config['REFRESH_SECRET_KEY'] = 'refreshsecretkey'
	app.config['SQLALCHEMY_DATABASE_URI'] = app_constants.DATABASE_PATH
	db.init_app(app)
	CORS(app)
	
	with app.app_context():
		db.create_all()

	return app

	
app = create_app()
jwt = JWTManager(app)
migrate = Migrate(app, db, compare_type=True)



# def token_required(f):
# 	@wraps(f)
# 	def decorated(*args, **kwargs):
# 		token = request.args.get('token') #query string
# 		print("This token is working fine!")

# 		if not token:
# 			return jsonify({'message' : 'Token is missing!'}), 403
# 		try:
# 			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
# 			#current_user = User.query.filter_by(email=data['email']).first()
# 		except:
# 			return jsonify({'message' : 'Token is invalid'}), 403

# 		return f(*args, **kwargs)

# 	return decorated

# NOTE: KART CLIENT 1.0
@app.route('/')
def index():
	# will have the ability to either login or look up an IGN
	return render_template("index.html")

# NOTE: KART CLIENT 1.0
@app.route('/signin', methods=['POST', 'GET']) #enable sign up
def signin():
	if request.method == 'POST':
		post_email = request.form['email']
		post_password = request.form['password']

		users = Users.query.filter_by(email=post_email).all()
		#current_user = User.query.filter_by(email=data['email']).first()
		if len(users) == 1:
			if util.is_user_password_valid(users[0], post_password):
				#access_token = jwt.encode({'user' : post_email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])
				access_token = create_access_token(identity = post_email, fresh = True)
				refresh_token = create_refresh_token(identity = post_email)
				#token_login = jsonify({'token' : token.decode('UTF-8')})
				#return jsonify({'token' : token.decode('UTF-8')})
				#return access_token
				return jsonify(access_token=access_token, refresh_token=refresh_token)
				#return token_login
				return render_template('account.html', name=users[0].ign)
	return render_template("signin.html")

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

# NOTE: KART CLIENT 1.0
@app.route('/signin/account/', methods=['POST', 'GET'])
def account():
	if request.method == 'POST':
		pass

	return render_template("account.html")

# NOTE: KART CLIENT 1.0
@app.route('/signin/account/chart')
def graph():
	return render_template('chart.html')

# NOTE: KART CLIENT 1.0
@app.route('/signin/account/records', methods=['POST', 'GET'])
@jwt_required()
#@token_required
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
				'쥐라기 공룡 결투장': request.form['map8_record'],
				'빌리지 남산': request.form['map9_record'],
			}
		}
		post_maps(post_data)

		return render_template("account.html")

	return render_template('records.html')

# NOTE: KART CLIENT 1.0
@app.route('/visitor')
def visitor():
	return render_template("visitor.html")

# NOTE: KART CLIENT 1.0
@app.route('/signin/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		post_email = request.form['email']
		post_ign = request.form['ign']
		post_password = request.form['password']
		post_confirm_password = request.form['confirm_password']
		if post_password == post_confirm_password:
			# TODO: Need to check if email exists already
			new_user = Users(email=post_email, password=util.hash_password(post_password), ign=post_ign)
			db.session.add(new_user)
			db.session.commit()
			return redirect('/signin')
		elif post_password != post_confirm_password:
			pass_list=[post_password,post_confirm_password]
			return render_template('signup.html', pass_list=pass_list)
	else:
		return render_template('signup.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
	if request.method == 'POST':
		res = post_sign_in(request.get_json())
		response = app.response_class(
			response=json.dumps(res),
			status=200,
			mimetype='application/json'
		)
		return response

@app.route('/sign_up', methods=['POST'])
def sign_up():
	if request.method == 'POST':
		res = post_sign_up(request.get_json())
		response = app.response_class(
			response=json.dumps(res),
			status=200,
			mimetype='application/json'
		)
		return response

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
#@token_required
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

@app.route('/elo')
def elo():
	ranking_dict = get_elo()
	response = app.response_class(
		response=json.dumps(ranking_dict),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/user_info')
def user_info():
	ign = request.args.get('ign')
	user_info_dict = get_user_info(ign)
	response = app.response_class(
		response=json.dumps(user_info_dict),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/map_levels')
def map_levels():
	map_levels = get_level_map_dict()
	response = app.response_class(
		response=json.dumps(map_levels),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/map_minimums')
def map_minimums():
	map_minimums = get_map_name_minimum_dict()
	response = app.response_class(
		response=json.dumps(map_minimums),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(foo="bar")

if __name__ == '__main__':
	app.run()