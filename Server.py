#!/usr/bin/env python2
from Adafruit_BNO055 import BNO055
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import logging
import time

app = Flask(__name__)
auth = HTTPBasicAuth()

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

users = {
    "pi": "raspberry"
}

commands = {
    'Id': 0,
    'Time':time.time(),
    'Armed': False,
    'Exit': False,
    'Snap': False,
    'Roll': 0.0,
    'RollKi':0.0,
    'RollKp':0.0,
    'RollKd':0.0,
    'Pitch': 0.0,
    'PitchKi':0.0,
    'PitchKp':0.0,
    'PitchKd':0.0,
    'Yaw': 0.0,
    'YawKi':0.0,
    'YawKp':0.0,
    'YawKd':0.0,
    'Throttle': 0.0,
    'ThrottleKi':0.0,
    'ThrottleKp':0.0,
    'ThrottleKd':0.0
}

observed = {
    'Id': 0,
    'Time':time.time(),
    'Armed': False,
    'Roll': 0.0,
    'RollKi':0.0,
    'RollKp':0.0,
    'RollKd':0.0,
    'RollError':0.0,
    'Pitch': 0.0,
    'PitchKi':0.0,
    'PitchKp':0.0,
    'PitchKd':0.0,
    'PitchError':0.0,
    'Yaw': 0.0,
    'YawKi':0.0,
    'YawKp':0.0,
    'YawKd':0.0,
    'YawError':0.0,
    'Throttle': 0.0,
    'ThrottleKi':0.0,
    'ThrottleKp':0.0,
    'ThrottleKd':0.0,
    'ThrottleError':0.0
}

last_update = time.time()

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
    # Verify Command Id is correct
    if commands['Id'] == commands_id:
        if ((not request.json) or
            ('Exit' in request.json and type(request.json['Exit']) is not bool) or
            ('Armed' in request.json and type(request.json['Armed']) is not bool) or
            ('Snap' in request.json and type(request.json['Armed']) is not bool) or
            ('Roll' in request.json and type(request.json['Roll']) is not float) or
            ('RollKi' in request.json and type(request.json['RollKi']) is not float) or
            ('RollKp' in request.json and type(request.json['RollKp']) is not float) or
            ('RollKd' in request.json and type(request.json['RollKd']) is not float) or
            ('Pitch' in request.json and type(request.json['Pitch']) is not float) or
            ('PitchKi' in request.json and type(request.json['PitchKi']) is not float) or
            ('PitchKp' in request.json and type(request.json['PitchKp']) is not float) or
            ('PitchKd' in request.json and type(request.json['PitchKd']) is not float) or
            ('Yaw' in request.json and type(request.json['Yaw']) is not float) or
            ('YawKi' in request.json and type(request.json['YawKi']) is not float) or
            ('YawKp' in request.json and type(request.json['YawKp']) is not float) or
            ('YawKd' in request.json and type(request.json['YawKd']) is not float) or
            ('Throttle' in request.json and type(request.json['Throttle']) is not float)):
            abort(400)
            
        commands['Time'] = time.time()
        commands['Exit'] = request.json.get('Exit', commands['Exit'])
        commands['Armed'] = request.json.get('Armed', commands['Armed'])
        commands['Snap'] = request.json.get('Snap', commands['Snap'])
        commands['Roll'] = request.json.get('Roll', commands['Roll'])
        commands['RollKi'] = request.json.get('RollKi', commands['RollKi'])
        commands['RollKp'] = request.json.get('RollKp', commands['RollKp'])
        commands['RollKd'] = request.json.get('RollKd', commands['RollKd'])
        commands['Pitch'] = request.json.get('Pitch', commands['Pitch'])
        commands['PitchKi'] = request.json.get('PitchKi', commands['PitchKi'])
        commands['PitchKp'] = request.json.get('PitchKp', commands['PitchKp'])
        commands['PitchKd'] = request.json.get('PitchKd', commands['PitchKd'])
        commands['Yaw'] = request.json.get('Yaw', commands['Yaw'])
        commands['YawKi'] = request.json.get('YawKi', commands['YawKi'])
        commands['YawKp'] = request.json.get('YawKp', commands['YawKp'])
        commands['YawKd'] = request.json.get('YawKd', commands['YawKd'])
        commands['Throttle'] = request.json.get('Throttle', commands['Throttle'])
        commands['ThrottleKi'] = request.json.get('ThrottleKi', commands['ThrottleKi'])
        commands['ThrottleKp'] = request.json.get('ThrottleKp', commands['ThrottleKp'])
        commands['ThrottleKd'] = request.json.get('ThrottleKd', commands['ThrottleKd'])

    else:
        not_found(404)
            
    return jsonify(commands)

@app.route('/observed', methods=['GET'])
@auth.login_required
def get_observed():   
    # Return Data as JSON
    return jsonify(observed)

@app.route('/shutdown', methods=['GET'])
@auth.login_required
def stop():
    raise RuntimeError("Server Shutdown requested...")

def flaskThread():
    try:
        # Run Server
        app.run(host='0.0.0.0')
    except RuntimeError, msg:
        print("Exiting Flask Thread becaue of runtime error")
        
