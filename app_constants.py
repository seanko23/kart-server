import os
from datetime import timedelta

TRIAL_CSV = 'trial.csv'
MAPS_CSV = 'maps.csv'

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'thisissecretkey')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
DATABASE_PATH = os.getenv('DATABASE_URL', 'postgresql://localhost/kart_server')

TEST_ACCOUNT_PASSWORD = '__sample__test__password__'