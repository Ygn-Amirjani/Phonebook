from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from

from models.User import User
from db import db

# Insert API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('phoneNumber', type=str, required=True)
parser.add_argument('username', type=str, required=True)

class Insert(Resource):
    @swag_from('../yml/insert.yml')
    def post(self):
        """ Use POST when you want to add a child resource under resources collection."""

        # Get new user information
        args = parser.parse_args()

        # id is made by default 
        phoneNumber = args['phoneNumber']
        username = args['username']

        message = ""
        # This condition is enforced when the given username does not exist in the table
        if len(User.query.filter_by(phoneNumber=phoneNumber).all()) >= 1:
            message = make_response(
                jsonify(msg="There is a user with this phone number in this database ..."), 403
            )
        else:
            # Write and save the information in the database 
            user = User(phoneNumber=phoneNumber, username=username)
            db.session.add(user)
            db.session.commit()

            message = make_response(
                jsonify(id=user.id,msg="Added New User"), 200
            )

        return message