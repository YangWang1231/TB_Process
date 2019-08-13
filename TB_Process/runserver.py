"""
This script runs the TB_Process application using a development server.
"""

from os import environ
from TB_Process import app
from TB_Process.config import Config

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    dir = Config.SQLALCHEMY_DATABASE_URI
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
