# HDI_dashboard
An HDI dashboard for movie fans to explore and manipulate movie data in different level of granularity.
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
- dash_bootstrap_components

## File structure
```
.
├── README.md
├── assets
│   └── style.css
├── load_data.sql
├── load_data_Neo4j.cql
├── movie.csv
├── server.py
└── src
    ├── backend
    │   ├── database_mongo.py
    │   ├── database_mysql.py
    │   └── database_neo4j.py
    ├── frontend
    │   ├── create_dash.py
    │   ├── overview.py
    │   └── schema.py
    └── main.py
```

## Set Up MySQL
1. Installed and started MySQL, reference to https://dev.mysql.com/doc/mysql-getting-started/en/
2. Connect to MySQL in terminal, i.e., `mysql -u root`
3. Copy and run all the statements in `load_data.sql`

## Compile
To start the dashboard, run:
```
cd src
python3 main.py
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
- The token used to connect with MongoDB Atlas is not commited into this repo due to concerns of data safety. Before compiling the program, please contact Xiaoying Zhu(xz45@illinois.edu) to get the token.
