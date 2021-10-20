import requests
import json
# import database, scrap, schema, query_parser
from flask import Flask, request, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
import database_mongo
import database_mysql

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def welcome():
    """
    Define message for base url
    :return: welcome message
    """
    return "HDI_dashboard"


@app.route(rule='/ratings', methods=['GET', 'PUT'])
def get_or_put_rating_vote():
    """
    GET: /ratings?id={id}, find rating count by movie's title id
    PUT: /ratings?id={id}, data is stored in json of request,
         update vote for rating by movie's title id

    :return: status code and message
    """
    title_id = check_id(request)
    if request.method == 'GET':
        result = database_mongo.find_by_id(title_id, 'Ratings')
        check_if_found(result)
        return jsonify(result[0]['weighted_average_vote']), 200
    else:
        check_content_type(request)
        new_data = request.json
        items = list(new_data.items())
        print(items)
        for item in items:
            key, var = item
            if key not in database_mongo.DOUBLE_ATTRI and key not in database_mongo.INT_ATTRI: \
                    abort(400, "Invalid attribute: " + key)

        status = database_mongo.update_data(title_id, new_data, "Ratings")
        if status == 0:
            return jsonify("rating with imdb_title_id: " + title_id + " has been updated."), 201
        elif status == 1:
            abort(400, "No ratings with such title_id.")
        elif status == 2:
            abort(400, "Unmatched field.")
        else:
            abort(400, "Invalid type of newValue.")


@app.route(rule='/movies', methods=['GET'])
def get_movies_by_conditions():
    """
    GET: /ratings?country={country}&year={year}&avg_vote={lower_bound},{upper_bound}&genre={genre}

    :return: status code and message
    """
    country = request.args.get('country', None)
    year = request.args.get('year', None)
    if year is not None:
        year = int(year)
    avg_vote = request.args.get('avg_vote', None)
    if avg_vote is not None:
        avg_vote = tuple([int(item) for item in avg_vote.split(',')])
    genre = request.args.get("genre", None)
    result = database_mysql.get_movies(country=country, year=year, avg_vote=avg_vote, genre=genre)
    return jsonify(result), 200


@app.route(rule='/countries', methods=['GET'])
def group_movies_by_countries():
    """
    GET: /countries, get total number of movies for each country

    :return: status code and message
    """
    result = database_mysql.group_movies_by_country()
    return jsonify(result), 200


def check_content_type(request):
    """
    Helper to check content type of request

    :param request: request need to be checked
    :return: no return value
    """
    if request.content_type != 'application/json':
        abort(415)


def check_id(curr_request):
    """
    Helper to check if a request contains id attribute
    :param curr_request: current request that is assumed to have id attribute

    :return: id if contains, abort otherwise
    """
    curr_id = curr_request.args.get('id', None)
    if not curr_id:
        abort(400, "Please specify id.")
    return curr_id


def check_if_found(result):
    if len(result) == 0:
        abort(404, "Record not found")


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'message': error.description}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': error.description}), 404)


@app.errorhandler(415)
def invalid_content_type(error):
    return make_response(jsonify({'message': "Data must be JSON."}), 415)

if __name__ == '__main__':
    app.run()
