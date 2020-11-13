from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import maps
import util.util as util

db = SQLAlchemy()

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), nullable=False, unique=True)
	password = db.Column(db.String(20), nullable=False)
	ign = db.Column(db.String(15), nullable=False, default='N/A', unique=True)
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
		return (f'MapRecords(users_id={self.users_id} map1={self.map1}) map2={self.map2}) map3={self.map3} ' +
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


def get_maps(filters={}):
	query = MapRecords.query
	if 'igns' in filters and filters['igns']:
		users = Users.query.filter(Users.ign.in_(set(filters['igns'])))
		users_ids = list(map(lambda user: user.id, users))
		query.filter(MapRecords.users_id.in_(users_ids))

	map_records = query.all()
	map_list = []
	for map_record in map_records:
		user_dict = {}
		for k, v in map_record.__dict__.items():
			if k[:3] == 'map' and v:
				user_dict[maps.convert_to_map_name(k)] = util.convert_to_time_string(v)
		user_dict['ign'] = map_record.users.ign
		map_list.append(user_dict)

	return {'data': map_list}
