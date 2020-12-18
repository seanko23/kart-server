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
	username = db.Column(db.String(40), nullable=False, unique=True)
	password = db.Column(db.String(40), nullable=False)
	ign = db.Column(db.String(30), nullable=False, default='N/A', unique=True)
	map_records = db.relationship('MapRecords', back_populates='users', uselist=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f'Users(username={self.username} password={self.password} ign={self.ign})'

class MapRecords(db.Model):
	__tablename__ = 'map_records'
	id = db.Column(db.Integer, primary_key=True)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	users = db.relationship('Users', back_populates='map_records')
	map1 = db.Column(db.Float, nullable=True)
	map2 = db.Column(db.Float, nullable=True)
	map3 = db.Column(db.Float, nullable=True)
	map4 = db.Column(db.Float, nullable=True)
	map5 = db.Column(db.Float, nullable=True)
	map6 = db.Column(db.Float, nullable=True)
	map7 = db.Column(db.Float, nullable=True)
	map8 = db.Column(db.Float, nullable=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return (f'MapRecords(users_id={self.users_id} map1={self.map1} map2={self.map2} map3={self.map3} ' +
            f'map4={self.map4} map5={self.map5} map6={self.map6} map7={self.map7} map8={self.map8})')


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

	db_keys = maps.get_valid_map_keys()
	df = df[db_keys + ['ign']].dropna(subset=db_keys)

	for db_key in db_keys:
		df[db_key] = df[db_key] - df[db_key].mean()

	df['record_sum'] = df[db_keys].sum(axis=1)
	mean_value = np.mean(df['record_sum'])

	df['normalized_sum'] = sklearn.preprocessing.scale(mean_value - df['record_sum'])
	df['elo'] = round(df['normalized_sum'] * 1000 + 5000)

	df = df.sort_values(by=['elo'], ascending=False)
	df['rank'] = [i + 1 for i in range(len(df))]

	return df


def get_elo():
	df = get_normalized_ranked_df()
	df = df[['rank', 'ign', 'elo']]
	return df.to_dict('records')


def get_home_info(ign):
	def format_rank_n_list(lst):
		return [maps.convert_to_map_name(x.replace('_rank_n', '')) for x in lst]

	if not ign:
		return {}
	elif len(Users.query.filter_by(ign=ign).all()) == 0:
		return {}

	home_info = {}
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
		if db_key in record_dict and record_dict[db_key]:
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

	return {
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
