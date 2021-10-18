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
    cursor = curr_db[collection_name].find({"imdb_title_id": "tt0000009"}, {"_id": False})
    # print(cursor.count())
    result = []
    for document in cursor:
        result.append(document)
    # print(result)
    return result

def get_movie_by_country(country):
    curr_db = connect_db()
    pipeline = [
       { "$match": { "country": country } },
       { "$group": { "_id": "$director", "total": { "$sum": 1 } } },
       { "$sort": { "total": -1} }
    ]
    cursor = curr_db["Movies"].aggregate(pipeline)
    # print(cursor.count())
    result = []
    for document in cursor:
        result.append(document)
    print(len(result))
    return result

def update_data(curr_id, new_data, collection_name):
    """
    Update current document by id

    :param curr_id: id of target document
    :param new_data: new newValue to update
    :param collection_name: name of target collection
    :return: 1 for no matched newValue, 0 for updated, 2 for updating error
    """
    curr_db = connect_db()
    cursor = curr_db[collection_name].find({'imdb_title_id': curr_id})
    print(curr_id)
    if cursor.count() == 0:
        return 1
    try:
        processed_data = {}
        for key, value in list(new_data.items()):
            if key in INT_ATTRI:
                processed_data[key] = int(value)
            elif key in DOUBLE_ATTRI:
                # print("value", value)
                processed_data[key] = float(value)
        print("processed:", processed_data)
        curr_db[collection_name].update_one(filter={'imdb_title_id': curr_id}, update={'$set': processed_data})
        return 0
    except pymongo.errors.WriteError:
        return 2
    except:
        return 3
