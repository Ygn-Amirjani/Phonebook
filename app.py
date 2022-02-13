from conf.flaskConfig import Config
from flask import Flask, jsonify
from flask_restful import Api
from src.models.user import User

from db import db

# Construct the core application.
app = Flask(__name__)
api = Api(app)

# configuration
app.debug = True
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    return jsonify("Just For Check :) ")


@app.before_first_request
def create_tables():
    """ To create/use the database mentioned in the URI, run this function. """ 
    User.__table__
    db.create_all()

if __name__ == '__main__':
    app.run()