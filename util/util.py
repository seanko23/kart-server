import bcrypt
from datetime import datetime as dt


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

def convert_to_int(timestamp):
    try:
        m, s, ss = map(lambda x: int(x), timestamp.split(":"))
        return m * 60 + s + ss / 100.0
    except:
        return False

def convert_to_time_string(float_time):
	return dt.strftime(dt.utcfromtimestamp(float_time), "%M:%S:%f")[:8]

def hash_password(password):
	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	return hashed.decode('utf-8')

def is_user_password_valid(user, password):
	hashed = user.password.encode('utf-8')
	password = password.encode('utf-8')
	return bcrypt.checkpw(password, hashed)
