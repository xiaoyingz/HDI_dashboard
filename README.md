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
- mysql

## Set Up MySQL 
1. Installed and started MySQL, reference to https://dev.mysql.com/doc/mysql-getting-started/en/git 
2. Create the movie table, by copying CREATE statement in load_data.sql
3. Import data from movie.csv to MySQL database using load command in load_data.sql

## Compile
To start the dashboard, run:
```
python3 app.py
```
## Files
- app.py: main program to render the dashboard
- database_mongo.py: contains helpers to fetch desired data from MongoDB Atlas
- load_data.sql: contains SQL commands to create table schema and upload data
- database_mysql.py: contains helpers to fetch and update desired data from MySQL 
- server.py: just for testing methods in database_mongo.py
- database_neo4j.py: contains helpers to fetch desired data from Neo4j Aura

## Notes
- The Neo4j is implemented on Neo4j AuraDB and it's commercial and collecting fees per hour. We have spent $30 on it. Closing the database will result in deletion on cloud, but we have to stop it after the Demo for saving money. If you want to implement the dashboard, please contact Lin Guo (linguo4@illinois.edu) to reinstall it.
