CREATE CONSTRAINT ON (m:Movie) ASSERT m.id IS UNIQUE;
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///IMDb_movies.csv' as row
             WITH row.imdb_title_id AS titleId, toFloat(row.avg_vote) AS avg_vote, row.original_title AS title, toInteger(row.year) AS year
	CREATE (m:Movie{id: titleId})      
             SET m.avg_vote=avg_vote    
 	SET m.title=title
	SET m.year = year   
             RETURN count(m);


CREATE CONSTRAINT ON (n:Name) ASSERT n.id IS UNIQUE;
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///IMDb_names.csv' as row1
             WITH row1.imdb_name_id AS nameId, row1.name AS name
	CREATE (n:Name{id: nameId})  
	SET n.name=name                
             RETURN count(n);


USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///IMDb_title_principals.csv' AS row2
WITH row2.imdb_title_id AS title_id, row2.imdb_name_id AS name_id, row2.category AS category
MATCH (m:Movie {id: title_id})
MATCH (n:Name {id: name_id})
MERGE (n)-[rel:PARTICIPATES {worktype: category}]->(m)
RETURN count(rel);
