from flask import jsonify
from flask_restful import Resource, reqparse, abort
from sqlalchemy import null
from models.User import User

from db import db

# Insert API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('phoneNumber', type=str, required=True)
parser.add_argument('username', type=str, required=True)

class Insert(Resource):
    def post(self):
        """ Use POST when you want to add a child resource under resources collection."""

        # Get new user information
        args = parser.parse_args()

        # id is made by default 
        phoneNumber = args['phoneNumber']
        username = args['username']

        # The phone number is a unique value and
        # it is not possible to store a phone number in the database for 2 different users
        self.abort_if_username_exist(phoneNumber=phoneNumber)

        # Write and save the information in the database 
        user = User(phoneNumber=phoneNumber, username=username)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"Added New User": username})

    def abort_if_username_exist(self, phoneNumber):
        """ The flask abort method either accepts an error code or it can accept a Response object. """
        if len(User.query.filter_by(phoneNumber=phoneNumber).all()) >= 1:
            abort(404,message="There is a user with this phone number in this database ...")