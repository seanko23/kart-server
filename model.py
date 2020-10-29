from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), nullable=False)
	password = db.Column(db.String(20), nullable=False)
	#ign = db.Column(db.String(15), nullable=False, default='N/A')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
        # TODO(seanko): Add ign here
		return f'User(username={self.username} password={self.password})'

class MapRecords(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ign = db.Column(db.String(15), nullable=False, default='N/A')
	map1 = db.Column(db.Float, nullable=False, default='N/A')
	map2 = db.Column(db.Float, nullable=False, default='N/A')
	map3 = db.Column(db.Float, nullable=False, default='N/A')
	map4 = db.Column(db.Float, nullable=False, default='N/A')
	map5 = db.Column(db.Float, nullable=False, default='N/A')
	map6 = db.Column(db.Float, nullable=False, default='N/A')
	map7 = db.Column(db.Float, nullable=False, default='N/A')
	map8 = db.Column(db.Float, nullable=False, default='N/A')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f'MapRecords(ign={self.ign} map1={self.map1}) map2={self.map2}) map3={self.map3} ' +
            f'map4={self.map4} map5={self.map5} map6={self.map6} map7={self.map7} map8={self.map8})'
