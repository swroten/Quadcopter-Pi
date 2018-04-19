#!/usr/bin/env python2
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "pi": "raspberry"
}

flightdata = {
    'CommandedRoll': 0.0,
    'CommandedPitch': 0.0,
    'CommandedYaw': 0.0,
    'CommandedThrottle': 0.0,
    'ObservedRoll': -1.0,
    'ObservedPitch': 0.543,
    'ObservedYaw': 0.987,
    'ObservedThrottle': 0.123
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

@app.route('/flightdata', methods=['GET'])
@auth.login_required
def get_flightdata():
    return jsonify({'FlightData':flightdata})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
