from app import db
from constants import TRIAL_CSV
from model import MapRecords
import pandas as pd
from util.util import record_to_int

def parse_record():
	df = pd.read_csv(TRIAL_CSV,sep=",")
	df = record_to_int(df)
	for index, row in df.iterrows():
		new_record = MapRecords(ign=row['IGN'], map1=row['map1'], map2=row['map2'], 
			map3=row['map3'], map4=row['map4'], map5=row['map5'], map6=row['map6'], 
			map7=row['map7'], map8=row['map8'])
		db.session.add(new_record)
		db.session.commit()

if __name__ == "__main__":
	parse_record()
