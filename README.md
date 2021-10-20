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
## Files
- app.py: main program to render the dashboard
- database_mongo.py: contains helpers to fetch desired data from MongoDB Atlas
- server.py: just for testing methods in database_mongo.py
- neo4j_import.py: import csv files to Neo4j AuraDB
