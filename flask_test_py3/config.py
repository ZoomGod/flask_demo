import os


DEBUG = True

SECRET_KEY = os.urandom(24)

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'a1b2c33.'
HOST = '47.100.211.202'
PORT = '3306'
DATABASE = 'flask_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME,
                                                                       PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
