from conf.flaskConfig import Config, CONFIG
from flask import Flask
from flask_restful import Api
from models.User import User
from business.Select import Select
from business.Insert import Insert

from db import db

# Construct the core application.
app = Flask(__name__)
api = Api(app)

# configuration
app.debug = True
app.config.from_object(Config)

db.init_app(app)

# Routes
api.add_resource(
    Select, 
    CONFIG.get('routes', {}).get('user', {}).get('select')
)
api.add_resource(
    Insert,
    CONFIG.get('routes', {}).get('user', {}).get('insert')
)

@app.before_first_request
def create_tables() -> None :
    """ To create/use the database mentioned in the URI, run this function. """ 
    User.__table__
    db.create_all()

if __name__ == '__main__':
    app.run(host=CONFIG.get('host'), port=CONFIG.get('port'))