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


def group_movies_by_country():
    cnx = mysql.connector.connect(user='root', database='mp', password='zxy971215')
    cursor = cnx.cursor()
    query = ("SELECT country, COUNT(imdb_title_id) FROM movie "
             "GROUP BY country")
    cursor.execute(query)
    counter = []
    for country, count in cursor:
        counter.append({'_id': country, 'total': count})
    cursor.close()
    cnx.close()
    return counter


if __name__ == '__main__':
    # movies = get_movies(country='China', year=2010, genre="Drama", avg_vote=(6, 8))
    # print(movies)
    counter = group_movies_by_country()
    print(counter)
