# kart-server

:)

Input the following lines in the correct folder of terminal to initialize the db:
1. from app import db, ModelName
2. db.create_all()

snake case
camel case


Running sqlite on terminal:
	sqlite3 records.db
	.tables
	select * from map_records;

relationship constraints

https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

one to one relationship


The Dataset may have to be restructured: Users Model should be filled in at once (includes ign)

Example Curl Requests to POST /maps
curl localhost:5000/maps \
-H "Content-Type: application/json" \
-d '{"ign":"seya", "maps": {"빌리지 고가의 질주": "1:40:51", "WKC 코리아 서킷": "1:50:50", "사막 빙글빙글 공사장": "2:40:51", "대저택 은밀한 지하실": "2:40:51", "노르테유 익스프레스": "2:40:51", "빌리지 운명의 다리": "2:40:51", "해적 로비 절벽의 전투": "2:40:51", "쥐라기 공룡 결투장": "2:40:51"}}'
