from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import pandas as pd

class App:

    def __init__(self):
        uri = "neo4j+s://6b402c80.databases.neo4j.io"
        user="neo4j"
        password="L1_1FT7yRIg1VB35sJQbpJ_BH8AM3iwf_Yv62CdMBY0"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    
    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def find_movie_from_person(self, person_name):
    # def find_movie_from_person(self, person_name, worktype, year_of_release, rating):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_movie, person_name)
            # result = session.read_transaction(self._find_and_return_movie, person_name, worktype, year_of_release, rating)
            # for row in result:
            #     print("Found movie: {row}".format(row=row))
            return result

    @staticmethod
    def _find_and_return_movie(tx, person_name):
    # def _find_and_return_movie(tx, person_name, worktype, year_of_release, rating):
        query = (
            "MATCH (n:Name)-[rel:PARTICIPATES]->(m:Movie) "
            "WHERE n.name = $person_name "
            # "WHERE n.name = $person_name AND rel.worktype = $worktype AND m.year >= $year_of_release AND m.avg_vote >= $rating"
            "RETURN m.title AS title, m.avg_vote AS rating, m.year AS year, rel.worktype AS worktype "
            "ORDER BY rating DESC"
        )
        result = tx.run(query, person_name=person_name)
        # return [row["title"] +"  Rating:"+ str(row["rating"]) +"  Release year:"+ str(row["year"]) +"  Worktype:"+ row["worktype"] for row in result]
        df = pd.DataFrame([r.values() for r in result], columns=result.keys())
        return df


    def update_rating(self, movie_id, avg_rating):
        with self.driver.session() as session:
            result = session.write_transaction(self._updata_rating_with_id, movie_id, avg_rating)
            for row in result:
                print("Found movie: {row}".format(row=row))


    @staticmethod
    def _updata_rating_with_id(tx, movie_id, avg_rating):
        query = (
            "MATCH (m:Movie {id: $movie_id}) "
            "SET m.avg_vote = $avg_rating "
            "RETURN m.title AS title, m.avg_vote as rating"
        )
        result = tx.run(query, movie_id=movie_id, avg_rating=avg_rating)
        try:
            return [row["title"] +"  Rating:"+ str(row["rating"]) for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        

# if __name__ == "__main__":
#     # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
#     uri = "neo4j+s://73def97d.databases.neo4j.io"
#     user = "neo4j"
#     password = "wivMop_vV-6GvErRjS6jI78237QfKRYK4T8J6NTCTqA"
#     app = App(uri, user, password)
#     result = app.find_movie_from_person("Philip Carli")
#     print(result)
#     app.update_rating("tt0042674",8.0)
#     app.close()