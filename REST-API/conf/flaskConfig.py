""" Flask configuration. """
import json

# Load config file
with open('./Phonebook/REST-API/conf/config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

# Database connection
database_username = CONFIG.get('database', {}).get('username')
database_password = CONFIG.get('database', {}).get('password')
database_server   = CONFIG.get('database', {}).get('server')
database_db       = CONFIG.get('database', {}).get('db')

# The database link to which it is connected .
database_uri = (f'mysql+pymysql://{database_username}:{database_password}@'
                f'{database_server}/{database_db}')

class Config :
    """ Set Flask config variables. """
    
    # The secret key is needed to keep the client-side sessions secure.
    SECRET_KEY = 'SuperSecretKey'
    # The database URI that should be used for the connection.
    SQLALCHEMY_DATABASE_URI = database_uri
    # If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.
    SQLALCHEMY_ECHO = False
    # If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals, The default is None.
    SQLALCHEMY_TRACK_MODIFICATIONS = False



