from app import db
from datetime import datetime


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), nullable=False, unique=True)
	password = db.Column(db.String(20), nullable=False)
	ign = db.Column(db.String(15), nullable=False, default='N/A', unique=True)
	map_record = db.relationship('MapRecords', backref='user', uselist=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
        # TODO(seanko): Add ign here
		return f'User(username={self.username} password={self.password})'

class MapRecords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	map1 = db.Column(db.Float, nullable=True)
	map2 = db.Column(db.Float, nullable=True)
	map3 = db.Column(db.Float, nullable=True)
	map4 = db.Column(db.Float, nullable=True)
	map5 = db.Column(db.Float, nullable=True)
	map6 = db.Column(db.Float, nullable=True)
	map7 = db.Column(db.Float, nullable=True)
	map8 = db.Column(db.Float, nullable=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	# def __repr__(self):
	# 	return f'MapRecords(ign={self.ign} map1={self.map1}) map2={self.map2}) map3={self.map3} ' +
    #         f'map4={self.map4} map5={self.map5} map6={self.map6} map7={self.map7} map8={self.map8})'
