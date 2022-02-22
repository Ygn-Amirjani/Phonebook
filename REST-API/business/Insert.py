from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
import sqlalchemy, logging

from models.User import User
from db import db

# Insert API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('phoneNumber', type=str, required=True)
parser.add_argument('username', type=str, required=True)

message = ""

class Insert(Resource):
    @swag_from('../yml/insert.yml')
    def post(self):
        """ Use POST when you want to add a child resource under resources collection."""

        # Get new user information
        args = parser.parse_args()

        # id is made by default 
        phoneNumber = args['phoneNumber']
        username = args['username']

        # Write and save the information in the database 
        user = User(phoneNumber=phoneNumber, username=username)
        db.session.add(user)
        try:
            db.session.commit()
            message = make_response(
                jsonify(msg="User Added ..."), 200
            )
        except sqlalchemy.exc.IntegrityError as e :
            message = make_response(
               jsonify(msg="I could not perform the desired operation. Please check the information and try again :)"), 500
            )
            logging.warning(e)
            
        return message