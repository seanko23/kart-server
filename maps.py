import constants
import pandas as pd
import util.util as util

db_keys = {}
map_names = {}
map_mins = {}
map_name_mins = {}
map_levels = {}
map_ratings = {}
level_maps = {}
level_names = ['스타선수', '랭커', '엘리트', '수준급', 'L1']
levels = ['R', 'L3', 'L2', 'L1']

def load_dicts():
    df = pd.read_csv(constants.MAPS_CSV)
    df['minimum_int'] = df.minimum.apply(util.convert_to_int)

    global db_keys, map_names, map_mins, map_name_mins, map_levels, map_ratings, level_maps, level_names
    db_keys = dict(zip(df.key, df.name))
    map_names = dict(zip(df.name, df.key))
    map_mins = dict(zip(df.key, df.minimum_int))
    map_name_mins = dict(zip(df.name, df.minimum))
    map_levels = dict(zip(df.key, df.level))

    for level in levels:
        level_maps[level] = list(df[df.level == level].name)

    map_ratings = df[['key'] + level_names] \
                    .set_index('key') \
                    .T \
                    .to_dict('list')
    for db_key in map_ratings:
        map_ratings[db_key] = list(map(lambda x: util.convert_to_int(x), map_ratings[db_key]))

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

def get_record_level(db_key, record):
    '''
    Usage: 
        get_record_level('map1', 90) -> '일반'
        get_record_level('map1', 100.99) -> '스타선수'
        get_record_level('map1', 100.98) -> '스타선수'
        get_record_level('map1', 101.00) -> '랭커'
        get_record_level('map1', 107.99) -> '수준급'
        get_record_level('map1', 109) -> 'L1'
        get_record_level('map1', 112) -> '일반'
        get_record_level('map2', 115.99) -> '수준급'
        get_record_level('map5', 112.99) -> '스타선수'
        get_record_level('map6', 131.22) -> '수준급'
        get_record_level('map7', 119.99) -> '엘리트'
        get_record_level('map8', 125.99) -> '일반'
    '''
    minimum = get_map_minimum(db_key)
    map_rating = map_ratings[db_key]
    rating = level_names + ['일반']

    for i in range(-1, -len(map_rating) - 1, -1):
        if map_rating[i] < record:
            return rating[i]
    return rating[0] if minimum < record else '일반'

def get_valid_map_keys():
    '''
    Usage: 
        get_valid_map_keys() -> ['map1', 'map2', ...]
    '''
    return list(db_keys)

def get_valid_map_names():
    '''
    Usage: 
        get_valid_map_keys() -> ['map1', 'map2', ...]
    '''
    return list(map_names)

def get_level_map_dict():
    '''
    Usage: 
        get_level_map_dict() -> {'R': ['빌리지 고가의 질주', '빌리지 남산', ...], 'L3': [...], ...}
    '''
    return level_maps

def get_map_name_minimum_dict():
    '''
    Usage: 
        get_map_name_minimum_dict() -> {
            '빌리지 고가의 질주': '01:35:00',
            'WKC 코리아 서킷': '01:45:00',
            ...
        }
    '''
    return map_name_mins

def get_map_level(db_key):
    '''
    Usage: 
        get_map_level('map1') -> 'R'
        get_map_level('map2') -> 'L3'
        get_map_level('map3') -> 'L2'
        get_map_level('map4') -> 'L2'
        get_map_level('map5') -> 'L1'
        get_map_level('map6') -> 'L3'
        get_map_level('invalid') -> False
    '''
    return map_levels[db_key] if db_key in map_levels else False

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

    assert(get_record_level('map1', 90) == '일반')
    assert(get_record_level('map1', 100.99) == '스타선수')
    assert(get_record_level('map1', 100.98) == '스타선수')
    assert(get_record_level('map1', 101.00) == '랭커')
    assert(get_record_level('map1', 107.99) == '수준급')
    assert(get_record_level('map1', 109) == 'L1')
    assert(get_record_level('map1', 112) == '일반')
    assert(get_record_level('map2', 115.99) == '수준급')
    assert(get_record_level('map5', 112.99) == '스타선수')
    assert(get_record_level('map6', 131.22) == '수준급')
    assert(get_record_level('map7', 119.99) == '엘리트')
    assert(get_record_level('map8', 125.99) == '일반')

    assert(get_map_level('map1') == 'R')
    assert(get_map_level('map2') == 'L3')
    assert(get_map_level('map3') == 'L2')
    assert(get_map_level('map4') == 'L2')
    assert(get_map_level('map5') == 'L1')
    assert(get_map_level('map6') == 'L3')
    assert(get_map_level('invalid') == False)
