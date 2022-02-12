""" Flask configuration. """

database_uri = 'mysql+pymysql://ArvanTestUser:ArvanCloudPassword@localhost/phonebook'

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

