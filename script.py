import pandas as pd
from app import MapRecords, db

def parse_record():
	df = pd.read_csv("trial.csv",sep=",")

	def record_to_int(df):

		column_names = list(df.columns)[1:]

		for i in column_names:
			measured_times = []
			for j in df[i]:     
				j = [int(z) for z in j.split(":")]
				updated_time = float(str(j[0]*60+j[1])+"."+str(j[2]))
				measured_times.append(updated_time)
			df[i] = measured_times
		return df

	df = record_to_int(df)


	for index, row in df.iterrows():
		# print(row)
		# print(row['map4'])
		# print(MapRecords(ign=row['IGN'], map1=row['map1'], map2=row['map2'], map3=row['map3'], map4=row['map4'], map5=row['map5'], map6=row['map6'], map7=row['map7'], map8=row['map8']))
		# break
		new_record = MapRecords(ign=row['IGN'], map1=row['map1'], map2=row['map2'], map3=row['map3'], map4=row['map4'], map5=row['map5'], map6=row['map6'], map7=row['map7'], map8=row['map8'])
		db.session.add(new_record)
		db.session.commit()

parse_record()
