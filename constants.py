import os

TRIAL_CSV = 'trial.csv'
MAPS_CSV = 'maps.csv'

DATABASE_PATH = os.getenv('DATABASE_URL', 'postgresql://localhost/kart_server')