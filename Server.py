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
    'Roll': 0.0,
    'Pitch': 0.0,
    'Yaw': 0.0,
    'Throttle': 0.0
}

observed = {
    'Id': 0,
    'Roll': -1.0,
    'Pitch': 0.543,
    'Yaw': 0.987,
    'Throttle': 0.123
}

# Throttle will be calculated later from feedback of the Engines
observedThrottle = 0

# Create IMU
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))


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
        if 'Roll' in request.json and type(request.json['Roll']) is not float:
            abort(400)
        if 'Pitch' in request.json and type(request.json['Pitch']) is not float:
            abort(400)
        if 'Yaw' in request.json and type(request.json['Yaw']) is not float:
            abort(400)
        if 'Throttle' in request.json and type(request.json['Throttle']) is not float:
            abort(400)
            
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
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()

    # Get Update Observed Data
    observed = {
        'Id': 0,
        'Roll': roll,
        'Pitch': pitch,
        'Yaw': heading,
        'Throttle': observedThrottle
    }
    
    # Return Data as JSON
    return jsonify(observed)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
