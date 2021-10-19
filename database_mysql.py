import mysql.connector
from collections import defaultdict

def get_movies(country=None, year=None, avg_vote=None, genre=None):
    """
    :return: a list of dictionary with key as field name
    """
    cnx = mysql.connector.connect(user='root', database='mp')
    cursor = cnx.cursor()
    query = ("SELECT * FROM movie "
         "WHERE country = %s")
    params = [country]
    if year is not None:
        query += " AND year = %s"
        params.append(year)
    if genre is not None:
        query += " AND genre = %s"
        params.append(genre)
    if avg_vote is not None:
        start, end = avg_vote
        query += " AND avg_vote >= %s AND avg_vote <= %s"
        params.extend([start, end])
    cursor.execute(query, tuple(params))
    fields = [i[0] for i in cursor.description]
    res = []
    for item in cursor:
        res.append(dict(zip(fields, item)))
    cursor.close()
    cnx.close()
    return res

movies = get_movies('China', year=2010, genre="Drama", avg_vote=(7,9))
print(movies)
