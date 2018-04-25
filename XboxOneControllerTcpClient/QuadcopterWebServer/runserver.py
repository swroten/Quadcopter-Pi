"""
This script runs the QuadcopterWebServer application using a development server.
"""

from os import environ
from QuadcopterWebServer import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')
