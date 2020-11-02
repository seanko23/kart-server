import constants
import pandas as pd
import util.util as util

db_keys = {}
map_names = {}
map_mins = {}

def load_dicts():
    df = pd.read_csv(constants.MAPS_CSV)
    df.minimum = df.minimum.apply(util.convert_to_int)

    global db_keys, map_names, map_mins
    db_keys = dict(zip(df.key, df.name))
    map_names = dict(zip(df.name, df.key))
    map_mins = dict(zip(df.key, df.minimum))

def convert_to_db_key(map_name):
    '''
    Usage: 
        convert_to_db_key('빌리지 고가의 질주') -> 'map1'
        convert_to_db_key('노르테유 익스프레스') -> 'map5'
        convert_to_db_key('invalid_key') -> False
    '''
    return map_names[map_name] if map_name in map_names else False

def convert_to_map_name(db_key):
    '''
    Usage: 
        convert_to_map_name('map1') -> '빌리지 고가의 질주'
        convert_to_map_name('map5') -> '노르테유 익스프레스'
        convert_to_map_name('invalid_key') -> False
    '''
    return db_keys[db_key] if db_key in db_keys else False

def get_map_minimum(db_key=None, map_name=None):
    '''
    Usage: 
        get_map_minimum(db_key='map1') -> 95.0
        get_map_minimum(map_name='빌리지 고가의 질주') -> 95.0

        get_map_minimum(map_name='map1') -> False
        get_map_minimum(db_key='빌리지 고가의 질주') -> False
        get_map_minimum(db_key='invalid_key') -> False
        get_map_minimum(db_key='map1', map_name='빌리지 고가의 질주') -> False
        get_map_minimum() -> False
    '''
    if map_name and db_key or not map_name and not db_key:
        return False

    if map_name:
        db_key = convert_to_db_key(map_name)

    return map_mins[db_key] if db_key in map_mins else False

def is_valid_record(map_name, record):
    '''
    Usage: 
        is_valid_record('빌리지 고가의 질주', '1:50:30') -> True
        is_valid_record('빌리지 고가의 질주', '10:50:30') -> True
        is_valid_record('빌리지 고가의 질주', '1:20:30') -> False
        is_valid_record('노르테유 익스프레스', '1:45:50') -> True
        is_valid_record('노르테유 익스프레스', 'invalid') -> False
        is_valid_record('노르테유 익스프레스', '1:45') -> False
        is_valid_record('invalid', '1:50:30') -> False
    '''
    int_record = util.convert_to_int(record)
    map_minimum = get_map_minimum(map_name=map_name)

    if not int_record or not map_minimum:
        return False

    return get_map_minimum(map_name=map_name) < int_record


load_dicts()
if __name__ == "__main__":
    assert convert_to_db_key('빌리지 고가의 질주') == 'map1'
    assert convert_to_db_key('노르테유 익스프레스') == 'map5'
    
    assert convert_to_map_name('map1') == '빌리지 고가의 질주'
    assert convert_to_map_name('map5') == '노르테유 익스프레스'

    assert get_map_minimum(db_key='map1') == 95.0
    assert get_map_minimum(map_name='빌리지 고가의 질주') == 95.0

    assert get_map_minimum(map_name='map1') == False
    assert get_map_minimum(db_key='빌리지 고가의 질주') == False
    assert get_map_minimum(db_key='invalid_key') == False
    assert get_map_minimum(db_key='map1', map_name='빌리지 고가의 질주') == False
    assert get_map_minimum() == False

    assert is_valid_record('빌리지 고가의 질주', '1:50:30') == True
    assert is_valid_record('빌리지 고가의 질주', '10:50:30') == True
    assert is_valid_record('빌리지 고가의 질주', '1:20:30') == False
    assert is_valid_record('노르테유 익스프레스', '1:45:50') == True
    assert is_valid_record('노르테유 익스프레스', 'invalid') == False
    assert is_valid_record('노르테유 익스프레스', '1:45') == False
    assert is_valid_record('invalid', '1:50:30') == False
    assert is_valid_record('invalid', 'invalid') == False
