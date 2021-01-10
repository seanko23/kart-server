# kart-server

:)

Input the following lines in the correct folder of terminal to initialize the db:
from app import app
from database import MapRecordLogs, MapRecords, Users, db
app.app_context().push()
db.create_all()

To add `trial.csv` records on the db:
```python
from app import app
from database import db
from util.scripts import create_sample_records, delete_sample_records
app.app_context().push()
delete_sample_records() # Delete records
create_sample_records() # Create records
```


snake case
camel case

<strike>
Running sqlite on terminal:
	sqlite3 records.db
	.tables
	select * from map_records;
</strike>

relationship constraints

https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

one to one relationship


The Dataset may have to be restructured: Users Model should be filled in at once (includes ign)

Example Curl Requests to POST /maps
curl localhost:5000/maps \
-H "Content-Type: application/json" \
-d '{"ign":"seya", "maps": {"빌리지 고가의 질주": "1:40:51", "WKC 코리아 서킷": "1:50:50", "사막 빙글빙글 공사장": "2:40:51", "대저택 은밀한 지하실": "2:40:51", "노르테유 익스프레스": "2:40:51", "빌리지 운명의 다리": "2:40:51", "해적 로비 절벽의 전투": "2:40:51", "쥐라기 공룡 결투장": "2:40:51"}}'

PostgreSQL local setup
https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-mac
- To connect to remote psql
 - heroku pg:psql
- To get heroku info
 - heroku pg:info
- To connect to local psql
 - psql
- To pull data from remote psql
 - heroku pg:pull HEROKU_POSTGRESQL_MAGENTA mylocaldb --app sushi
- To push data to remote psql
 - heroku pg:push mylocaldb HEROKU_POSTGRESQL_MAGENTA --app sushi


 Heroku Cheatsheet
 - To see server log
  - heroku logs -t
- To push changes on heroku
 - git push heroku main

Flask Migrate Cheatsheet (https://flask-migrate.readthedocs.io/en/latest/)
- To add a new column to db
 - add a new column on the table in database.py
 - `flask db migrate -m "<Description of the database change>"`
 - `flask db upgrade` (This will apply changes on local db)
 - After this, the db needs to be updated for the production database on heroku
- To apply new changes on db
 - `flask db upgrade`
 - `heroku run flask db upgrade`

PostgreSQL Update Trigger
- Whenever there is a create/update operation on MapRecords, a record of `map_record_logs` will be created.
- Set up
 - copy and paste `util/trigger_function.sql` in psql terminal
 - copy and paste `util/create_trigger.sql` in psql terminal