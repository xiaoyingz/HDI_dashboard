import os
import mysql.connector
from collections import defaultdict
import dotenv
from pathlib import Path

dotenv_path = Path('/Users/zhuxiaoying/Desktop/cs511_project/.env')
env = dotenv.load_dotenv(dotenv_path='/Users/zhuxiaoying/Desktop/cs511_project/.env', verbose=True, override=False)
password=os.getenv('PASSWORD')
password = "zxy971215"
def get_movies(country=None, year=None, avg_vote=None, genre=None, order='DESC'):
    """
    :return: a list of dictionary with key as field name
    """
    cnx = mysql.connector.connect(user='root', database='mp', password=password)
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
    query += " ORDER BY avg_vote "+order
    cursor.execute(query, tuple(params))
    fields = [i[0] for i in cursor.description]
    res = []
    for item in cursor:
        res.append(dict(zip(fields, item)))
    cursor.close()
    cnx.close()
    return res


def group_movies_by_country():
    cnx = mysql.connector.connect(user='root', database='mp', password=password)
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

def group_movies_by_genre(country):
    #group by genre, given country   ->{genre:num}
    cnx = mysql.connector.connect(user='root', database='mp', password=password)
    cursor = cnx.cursor()
    query = ("SELECT genre, COUNT(imdb_title_id) FROM movie "
             "WHERE country = %s "
             "GROUP BY genre ")
    cursor.execute(query, (country,))
    counter = {}
    for genre, count in cursor:
        counter[genre] = count
    cursor.close()
    cnx.close()
    return counter

def get_id_by_name(movie_title, original=True):
    """
    :param movie_title: the title of movie
    :param original: whether use title or original_title, default is using original_title
    :return: dict {field_name:val} movie information
    """
    cnx = mysql.connector.connect(user='root', database='mp', password=password)
    cursor = cnx.cursor()
    if original:
        query = ("SELECT * FROM movie "
                "WHERE original_title = %s ")
    else:
        query = ("SELECT * FROM movie "
                 "WHERE title = %s ")
    cursor.execute(query, (movie_title,))
    fields = [i[0] for i in cursor.description]
    res = None
    for item in cursor:
        res = dict(zip(fields, item))
        break
    cursor.close()
    cnx.close()
    return res

def update_avg_vote(movie_id, avg_vote):
    """
    update the average voting of a movie given movie_id
    :return: updated data {movie_id:{}, avg_vote:{}}
    """
    cnx = mysql.connector.connect(user='root', database='mp', password=password)
    cursor = cnx.cursor()
    query = ("UPDATE movie "
             "SET avg_vote = %s "
             "WHERE imdb_title_id = %s ")
    cursor.execute(query, (avg_vote, movie_id))
    cnx.commit()
    query = ("SELECT imdb_title_id, avg_vote FROM movie "
             "WHERE imdb_title_id = %s ")
    cursor.execute(query, (movie_id,))
    fields = [i[0] for i in cursor.description]
    res = None
    for item in cursor:
        res = dict(zip(fields, item))
        break
    cursor.close()
    cnx.close()
    if res is None or res['imdb_title_id'] != movie_id or res['avg_vote'] != avg_vote:
        return -1
    return res

if __name__ == '__main__':
    movies = get_movies(country='USA', year=2010, genre="Drama", avg_vote=(6, 8))
    print(movies)
    # counter = group_movies_by_country()
    # #print(counter)
    # counter = group_movies_by_genre('China')
    # #print(counter)
    # movie = get_id_by_name('Biancaneve e i sette nani', False)
    # #print(movie)
    # movie = get_id_by_name('Snow White and the Seven Dwarfs')
    # #print(movie)
    # info = update_avg_vote("tt0027977", 9.0)
    # print(info)
    # movie = get_id_by_name('Tempi moderni', False)
    # print(movie)
    # print(get_movies(country='Brazil', year=1985, avg_vote=(5,8), genre='Drama'))
