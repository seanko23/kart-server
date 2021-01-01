from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
import sklearn
import numpy as np

import constants
import maps
import util.util as util

db = SQLAlchemy()
engine = sqlalchemy.create_engine(constants.DATABASE_PATH)

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(320), nullable=False, unique=True)
	password = db.Column(db.String(40), nullable=False)
	ign = db.Column(db.String(30), nullable=False, default='N/A', unique=True)
	map_records = db.relationship('MapRecords', back_populates='users', uselist=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	visitor_count = db.Column(db.Integer, default=0)

	def __repr__(self):
		return f'Users(email={self.email} password={self.password} ign={self.ign})'

class MapRecords(db.Model):
	__tablename__ = 'map_records'
	id = db.Column(db.Integer, primary_key=True)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	users = db.relationship('Users', back_populates='map_records')
	map1 = db.Column(db.Float, nullable=True) # 빌리지 고가의 질주
	map2 = db.Column(db.Float, nullable=True) # WKC 코리아 서킷
	map3 = db.Column(db.Float, nullable=True) # 사막 빙글빙글 공사장
	map4 = db.Column(db.Float, nullable=True) # 대저택 은밀한 지하실
	map5 = db.Column(db.Float, nullable=True) # 노르테유 익스프레스
	map6 = db.Column(db.Float, nullable=True) # 빌리지 운명의 다리
	map7 = db.Column(db.Float, nullable=True) # 해적 로비 절벽의 절투
	map8 = db.Column(db.Float, nullable=True) # 쥐라기 공룡 결투장
	map9 = db.Column(db.Float, nullable=True) # 빌리지 남산
	map10 = db.Column(db.Float, nullable=True) # 비치 해변 드라이브
	map11 = db.Column(db.Float, nullable=True) # WKC 싱가폴 서킷
	map12 = db.Column(db.Float, nullable=True) # 1920 아슬아슬 비행장
	map13 = db.Column(db.Float, nullable=True) # 차이나 라사
	map14 = db.Column(db.Float, nullable=True) # 월드 두바이 다운타운
	map15 = db.Column(db.Float, nullable=True) # 도검 야외수련관
	map16 = db.Column(db.Float, nullable=True) # 빌리지 손가락
	map17 = db.Column(db.Float, nullable=True) # 월드 리오 다운힐
	map18 = db.Column(db.Float, nullable=True) # 문힐시티 폭우속의 질주
	map19 = db.Column(db.Float, nullable=True) # 메카닉 잊혀진 도시의 중심부
	map20 = db.Column(db.Float, nullable=True) # 도검 용의 길
	map21 = db.Column(db.Float, nullable=True) # 네모 장난감 선물공장
	map22 = db.Column(db.Float, nullable=True) # 차이나 서안 병마용
	map23 = db.Column(db.Float, nullable=True) # 빌리지 만리장성
	map24 = db.Column(db.Float, nullable=True) # 님프 바다신전의 비밀
	map25 = db.Column(db.Float, nullable=True) # 포레스트 지그재그
	map26 = db.Column(db.Float, nullable=True) # WKC 브라질 서킷
	map27 = db.Column(db.Float, nullable=True) # 차이나 황산
	map28 = db.Column(db.Float, nullable=True) # 해적 숨겨진 보물
	map29 = db.Column(db.Float, nullable=True) # 빌리지 붐힐터널
	map30 = db.Column(db.Float, nullable=True) # 황금문명 비밀장치의 위협
	map31 = db.Column(db.Float, nullable=True) # 아이스 갈라진 빙산
	map32 = db.Column(db.Float, nullable=True) # 네모 산타의 비밀공간
	map33 = db.Column(db.Float, nullable=True) # 동화 이상한 나라의 문
	map34 = db.Column(db.Float, nullable=True) # 광산 꼬불꼬불 다운힐
	map35 = db.Column(db.Float, nullable=True) # 팩토리 미완성 5구역
	map36 = db.Column(db.Float, nullable=True) # 포레스트 아찔한 다운힐
	map37 = db.Column(db.Float, nullable=True) # 공동묘지 마왕의 초대
	map38 = db.Column(db.Float, nullable=True) # 아이스 설산 다운힐
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return (f'MapRecords(users_id={self.users_id} map1={self.map1} map2={self.map2} map3={self.map3} ' +
            f'map4={self.map4} map5={self.map5} map6={self.map6} map7={self.map7} map8={self.map8}...)')

def post_sign_in(data):
	email, password = data['email'], data['password']
	if not email or not password:
		return {'error': 'email or password should not be empty'}

	user = Users.query.filter_by(email=email, password=password).first()
	if not user:
		return {'error': 'email or password is incorrect'}
	return {
		'error': '',
		'user': {'ign': user.ign}
	}

def post_sign_up(data):
	email, password, ign = data['email'], data['password'], data['ign']
	if not email or not password or not ign:
		return {'error': 'email, password, ign should not be empty'}

	email_user = Users.query.filter_by(email=email).first()
	ign_user = Users.query.filter_by(ign=ign).first()
	if email_user:
		return {'error': f'Email {email} already exists'}
	elif ign_user:
		return {'error': f'Nickname {ign} already exists'}
	
	user = Users(email=email, password=password, ign=ign)
	db.session.add(user)
	db.session.commit()

	return {
		'error': '',
		'user': {'ign': user.ign}
	}

def post_maps(map_data):
	ign, maps_data = map_data['ign'], map_data['maps']

	map_records = {}
	for map_name, record in maps_data.items():
		if not record:
			continue
		elif maps.is_valid_record(map_name, record):
			map_records[maps.convert_to_db_key(map_name)] = util.convert_to_int(record)
		else:
			raise ValueError('invalid record: {} {}'.format(map_name, record))

	users = Users.query.filter_by(ign=ign).all()
	if len(users) > 1:
		raise ValueError('There should not be more than one record of user for each ign. ign: {}'.format(ign))
	elif len(users) == 0:
		raise ValueError('No user exists. ign: {}'.format(ign))
	user = users[0]

	map_models = MapRecords.query.filter_by(users=user)
	map_models_results = map_models.all()
	if len(map_models_results) > 1:
		raise ValueError('There should not be more than one record for each ign. ign: {} user_id: {}'.format(ign, user.id))

	if not map_models_results:
		map_records['users'] = user
		map_record = MapRecords(**map_records)
		db.session.add(map_record)
	else:
		map_models.update(map_records)

	db.session.commit()
	return True


def get_maps_by_users(filters={}):
	query = MapRecords.query
	if 'igns' in filters and filters['igns']:
		users = Users.query.filter(Users.ign.in_(set(filters['igns'])))
		users_ids = set(map(lambda user: user.id, users))
		map_records = query.filter(MapRecords.users_id.in_(users_ids))
	else:
		map_records = query.all()
	map_list = []
	for map_record in map_records:
		user_dict = {}
		for k, v in map_record.__dict__.items():
			if k[:3] == 'map' and v:
				user_dict[maps.convert_to_map_name(k)] = util.convert_to_time_string(v)
		user_dict['ign'] = map_record.users.ign
		map_list.append(user_dict)

	return map_list


def get_maps_by_map(map_name):
	db_key = maps.convert_to_db_key(map_name)
	if db_key:
		map_records = MapRecords.query \
								.filter(getattr(MapRecords, db_key) != None) \
								.order_by(getattr(MapRecords, db_key))

		user_list = []
		for i, map_record in enumerate(map_records):
			user_list.append({
				'rank': i + 1,
				'ign': map_record.users.ign,
				'record': util.convert_to_time_string(getattr(map_record, db_key)),
			})
		return user_list
	return {}


# NOTE: returns records df
def get_records_df():
	Session = sessionmaker(bind = engine)
	session = Session()

	query = session.query(MapRecords, Users).filter(MapRecords.users_id == Users.id)
	df = pd.read_sql(query.statement, query.session.bind)
	return df


# NOTE: returns records df with record_sum, normalized_sum, elo and elo rank
def get_normalized_ranked_df():
	df = get_records_df()

	records_to_keep = 8
	db_keys = maps.get_valid_map_keys()
	ign = df['ign']
	df = df[db_keys] # Drop useless columns
	df = df.loc[df.count(axis=1) >= records_to_keep] # Drop all users with less than 8 map_records data

	for db_key in db_keys:
		df[db_key] = df[db_key] - df[db_key].mean()

	record_sum = []
	for record in df.to_numpy():
		record = record[~pd.isnull(record)] # Drop all null values
		record_sum.append((sum(np.sort(record)[:records_to_keep]))) # Keep the best 8 records

	df['record_sum'] = pd.Series(record_sum, index=df.index)
	mean_value = np.mean(df['record_sum'])

	df['normalized_sum'] = sklearn.preprocessing.scale(mean_value - df['record_sum'])
	df['elo'] = round(df['normalized_sum'] * 1000 + 5000)
	df['ign'] = ign

	df = df.sort_values(by=['elo'], ascending=False)
	df['rank'] = [i + 1 for i in range(len(df))]

	return df


def get_elo():
	df = get_normalized_ranked_df()
	df = df[['rank', 'ign', 'elo']]
	return df.to_dict('records')


def get_user_info(ign):
	def format_rank_n_list(lst):
		return [maps.convert_to_map_name(x.replace('_rank_n', '')) for x in lst]

	response = {'is_user_registered': False, 'records_data': {}}
	if not ign:
		return response
	elif len(Users.query.filter_by(ign=ign).all()) != 1:
		return response

	response['is_user_registered'] = True
	if not Users.query.filter_by(ign=ign).first().map_records:
		return response

	df = get_records_df()
	db_keys = maps.get_valid_map_keys()
	num_records = {}
	for db_key in db_keys:
		num_rows, db_key_rank = int(df[db_key].count()), df[db_key].rank(method='min')
		df[db_key + '_rank'] = db_key_rank
		df[db_key + '_rank_n'] = db_key_rank / num_rows
		num_records[maps.convert_to_map_name(db_key)] = num_rows

	series = df[df.ign == ign].iloc[0]
	record_dict = series.to_dict()
	map_records = {}
	rank_records = {}
	level_records = {}
	map_levels = {}
	for db_key in db_keys:
		if db_key in record_dict and record_dict[db_key] and not np.isnan(record_dict[db_key]):
			map_name = maps.convert_to_map_name(db_key)
			map_records[map_name] = util.convert_to_time_string(record_dict[db_key])
			rank_records[map_name] = int(record_dict[db_key + '_rank'])
			level_records[map_name] = maps.get_record_level(db_key, record_dict[db_key])
			map_levels[map_name] = maps.get_map_level(db_key)

	db_keys_n = list(map(lambda x: x + '_rank_n', db_keys))
	n_series = series[db_keys_n]
	record_std = n_series.std()

	# NOTE: under/over_performing_maps compared to user's other records
	# NOTE: User is under/over-performing if his record is over the range of 1 standard deviation (68%)
	# NOTE: Refer to https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-data-frame
	under_performing_map = format_rank_n_list(n_series[n_series-n_series.mean() > record_std].index)
	over_performing_map = format_rank_n_list(n_series[n_series.mean() - n_series > record_std].index)

	# NOTE: upper 25%, upper 25-50% and bottom 50% of user's records compared to other users
	high_25 = format_rank_n_list(n_series[n_series <= 0.25].index)
	high_50 = format_rank_n_list(n_series[n_series <= 0.5].index)
	low_50 = format_rank_n_list(n_series[n_series > 0.5].index)
	high_25_50 = list(set(high_50) - set(high_25))
	
	response['records_data'] = {
		'under_performing_map': under_performing_map,
		'over_performing_map': over_performing_map,
		'high_25': high_25,
		'high_25_50': high_25_50,
		'low_50': low_50,
		'map_records': map_records,
		'rank_records': rank_records,
		'num_records': num_records,
		'level_records': level_records,
		'map_levels': map_levels,
	}
	return response
