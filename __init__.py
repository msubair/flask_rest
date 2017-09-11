#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from dota2test_function import *

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'dota2':
#         return 'test'
#     return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
#     # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify( { 'error': 'Internal Server Error' } ), 500)

@app.route('/dota2test/api/v0.1/rangking', methods=['POST'])
# @auth.login_required
def get_rangking():
    if not request.json or not 'users' in request.json:
        abort(400)
    users = request.json['users']
    return_data = get_return_wl_data(users)
    final_data = get_final_rangking(return_data)
    return jsonify({'result': final_data})

@app.route('/dota2test/api/v0.1/comparison', methods=['POST'])
# @auth.login_required
def get_comparison():
    if not request.json or not 'users' in request.json or len(request.json['users']) != 2:
        abort(400)
    users = request.json['users']
    return_data = get_return_total_data(users)
    final_data = get_final_comparison(return_data)
    return jsonify({'result': final_data})

@app.route('/dota2test/api/v0.1/heroforuser/<string:user_id>', methods = ['GET'])
# @auth.login_required
def get_hero_for_user(user_id):
    return_data = get_heroes(user_id)
    if return_data == False:
        abort(404)
    final_data = get_best_hero(return_data)
    if final_data == False:
        abort(404)
    return jsonify({'result': final_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug = True)