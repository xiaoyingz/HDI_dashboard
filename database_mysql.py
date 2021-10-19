import mysql.connector
from collections import defaultdict


def get_movies(country=None, year=None, avg_vote=None, genre=None):
    """
    :return: a list of dictionary with key as field name
    """
    cnx = mysql.connector.connect(user='root', database='mp')
    cursor = cnx.cursor()
    query = "SELECT * FROM movie"
    conditions = []
    params = []
    if country is not None:
        conditions.append("country = %s")
        params.append(country)
    if year is not None:
        conditions.append("year = %s")
        params.append(year)
    if genre is not None:
        conditions.append("genre = %s")
        params.append(genre)
    if avg_vote is not None:
        conditions.append("avg_vote >= %s AND avg_vote <= %s")
        start, end = avg_vote
        params.extend([start, end])
    if conditions:
        query += " WHERE "
        query += " AND ".join(conditions)
    cursor.execute(query, tuple(params))
    fields = [i[0] for i in cursor.description]
    res = []
    for item in cursor:
        res.append(dict(zip(fields, item)))
    cursor.close()
    cnx.close()
    return res

if __name__ == '__main__':
    movies = get_movies(country='China', year=2010, genre="Drama", avg_vote=(6, 8))
    print(movies)
