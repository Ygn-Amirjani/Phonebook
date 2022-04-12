from flask import Flask
from flask_restful import Api
from flasgger import Swagger
import sqlalchemy, logging, sys

from swaggerTemplate import template
from models.User import User
from conf.flaskConfig import Config, CONFIG
from business.Select import Select
from business.Insert import Insert
from business.Delete import Delete
from business.Update import Update

from db import db

# Construct the core application.
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template=template)

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
    CONFIG.get('routes', {}).get('user', {}).get('main')
)
api.add_resource(
    Delete,
    CONFIG.get('routes', {}).get('user', {}).get('main')
)
api.add_resource(
    Update,
    CONFIG.get('routes', {}).get('user', {}).get('update')
)

@app.before_first_request
def create_tables() -> None :
    """ To create/use the database mentioned in the URI, run this function. """ 
    
    logging.basicConfig(filename='/var/log/restapi/app.log', format='%(asctime)s - [%(levelname)s] - %(message)s',  
    datefmt='%d-%b-%y %H:%M:%S')
    User.__table__
    try:
        db.create_all()
    except sqlalchemy.exc.OperationalError as e:
        logging.error(e)
        sys.exit()

if __name__ == '__main__':
    app.run(host=CONFIG.get('host'), port=CONFIG.get('port'))