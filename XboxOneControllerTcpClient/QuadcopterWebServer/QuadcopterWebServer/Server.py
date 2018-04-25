#!/usr/bin/env python2
from Adafruit_BNO055 import BNO055
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "pi": "raspberry"
}

commands = {
    'Id': 0,
    'Exit': False,
    'Roll': 0.0,
    'Pitch': 0.0,
    'Yaw': 0.0,
    'Throttle': 0.0
}

observed = {
    'Id': 0,
    'Roll': 0.0,
    'Pitch': 0.0,
    'Yaw': 0.0,
    'Throttle': 0.0
}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

@app.route('/commands/<int:commands_id>', methods=['PUT'])
@auth.login_required
def update_commands(commands_id):
    
    if commands['Id'] == commands_id:
        if not request.json:
            abort(400)
        if 'Exit' in request.json and type(request.json['Exit']) is not bool:
            abort(400)
        if 'Roll' in request.json and type(request.json['Roll']) is not float:
            abort(400)
        if 'Pitch' in request.json and type(request.json['Pitch']) is not float:
            abort(400)
        if 'Yaw' in request.json and type(request.json['Yaw']) is not float:
            abort(400)
        if 'Throttle' in request.json and type(request.json['Throttle']) is not float:
            abort(400)
            
        commands['Exit'] = request.json.get('Exit', commands['Exit'])
        commands['Roll'] = request.json.get('Roll', commands['Roll'])
        commands['Pitch'] = request.json.get('Pitch', commands['Pitch'])
        commands['Yaw'] = request.json.get('Yaw', commands['Yaw'])
        commands['Throttle'] = request.json.get('Throttle', commands['Throttle'])

    else:
        not_found(404)
    
    return jsonify(commands)

@app.route('/observed', methods=['GET'])
@auth.login_required
def get_observed():
    # Return Data as JSON
    return jsonify(observed)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
