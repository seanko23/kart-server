from app import app
from constants import TRIAL_CSV, TEST_ACCOUNT_PASSWORD
from database import MapRecords, Users, db
import pandas as pd
from util.util import record_to_int

def create_sample_records():
	df = pd.read_csv(TRIAL_CSV,sep=",")
	df = record_to_int(df)
	for index, row in df.iterrows():
		new_user = Users(
			email=row['IGN'] + '@test2.com',
			password=TEST_ACCOUNT_PASSWORD,
			ign=f'__{row["IGN"]}__'
		)
		db.session.add(new_user)

		new_record = MapRecords(users=new_user, map1=row['map1'], map2=row['map2'], 
			map3=row['map3'], map4=row['map4'], map5=row['map5'], map6=row['map6'], 
			map7=row['map7'], map8=row['map8'])
		db.session.add(new_record)
		db.session.commit()
		print('{} Added user record for ign: {}'.format(index + 1, f'__{row["IGN"]}__'))
	print('Created sample records')

def delete_sample_records():
	users = Users.query.filter_by(password=TEST_ACCOUNT_PASSWORD)
	users_ids = set(map(lambda usr: usr.id, users))
	map_records = MapRecords.query.filter(MapRecords.users_id.in_(users_ids))

	map_records.delete(synchronize_session=False)
	users.delete()
	db.session.commit()
	print('Deleted sample records')

if __name__ == "__main__":
	app.app_context().push()
	create_sample_records()
	delete_sample_records()
