# HDI_dashboard
## Environment:
Python 3.8.5
## Dependencies:
- dash
- pandas
- plotly
- pymongo
- dotenv
- neo4j
- mysql-connector-python
## Compile
To start the dashboard, run:
```
python3 app.py
```
To start the dashboard for neo4j, run:
```
python app_neo4j.py
```
## Files
- app.py: main program to render the dashboard
- database_mongo.py: contains helpers to fetch desired data from MongoDB Atlas
- server.py: just for testing methods in database_mongo.py
- app_neo4j.py main program to render the neo4j dashboard
- database_neo4j.py: contains helpers to fetch desired data from Neo4j Aura
