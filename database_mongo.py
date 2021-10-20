import os
import sys
import json
from collections import OrderedDict
import pymongo
from pymongo import MongoClient
import dotenv
from pathlib import Path

dotenv_path = Path('/Users/zhuxiaoying/Desktop/cs511_project/.env')
env = dotenv.load_dotenv(dotenv_path='/Users/zhuxiaoying/Desktop/cs511_project/.env', verbose=True, override=False)
MONGOURL = os.getenv('MONGOURL')
DOUBLE_ATTRI = ['weighted_average_vote', 'mean_vote']
INT_ATTRI = ['total_votes']
for i in range(1, 11):
    INT_ATTRI.append('votes_'+str(i))

def connect_db():
    # load_dotenv(dotenv_path=dotenv_path)
    client = MongoClient(MONGOURL)
    print(MONGOURL)
    print("connected")
    return client["Movies"]

def find_by_id(curr_id, collection_name):
    """
    Find rating by title_id.

    :param title_id: movie's title_id the rating belongs to
    :return: list of result
    """
    curr_db = connect_db()
    # print(curr_db[collection_name].count())
    # print(type(curr_id))
    # print(collection_name)
    cursor = curr_db[collection_name].find({"_id": curr_id}, {"_id": False})
    # print(cursor.count())
    return cursor_to_list(cursor)

def get_movie_by_country(country):
    curr_db = connect_db()
    pipeline = [
       { "$match": { "country": country } },
       { "$group": { "_id": "$director", "total": { "$sum": 1 } } },
       { "$sort": { "total": -1} }
    ]
    cursor = curr_db["Movies"].aggregate(pipeline)
    # print(cursor.count())
    return cursor_to_list(cursor)

def group_movie_by_country():
    curr_db = connect_db()
    pipeline = [
       { "$group": { "_id": "$country", "total": { "$sum": 1 } } },
       { "$sort": { "total": -1} }
    ]
    cursor = curr_db["Movies"].aggregate(pipeline)
    return cursor_to_list(cursor)

def update_rating(curr_id, vote, collection_name='Ratings'):
    """
    Update current document by id

    :param curr_id: id of target document
    :param vote: new newValue to update
    :param collection_name: name of target collection
    :return: -1 for errors, otherwise newly calculated mean_vote
    """
    curr_db = connect_db()
    cursor = curr_db[collection_name].find({'_id': curr_id})
    if cursor.count() == 0:
        print("no such id")
        return -1
    try:
        vote_num = int(vote)
        if vote_num <= 0 or vote_num > 10:
            print("invalid vote number")
            return -1

        field = 'votes_'+vote
        curr_record = cursor_to_list(cursor)[0]

        prev_total = curr_record['total_votes']
        new_votes = curr_record[field]+1
        new_sum = curr_record['mean_vote']*prev_total+vote_num
        new_total = prev_total+1
        new_mean = float(format(new_sum/new_total, ".1f"))

        update_data = {'mean_vote': new_mean, 'total_votes': new_total, field: new_votes}
        print("processed:", update_data)
        curr_db[collection_name].update_one(filter={'_id': curr_id}, update={'$set': update_data})
        return new_mean
    except ValueError:
        print("invalid format of vote")
        return -1
    except pymongo.errors.WriteError:
        print("WriteError")
        return -1

def cursor_to_list(cursor):
    result = []
    for document in cursor:
        result.append(document)
    # print(result)
    return result

if __name__ == "__main__":
    print(update_rating("tt0000009", '10'))
