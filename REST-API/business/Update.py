from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from

from models.User import User
from db import db

# Update API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id', type=int, required=True)
parser.add_argument('username', type=str, required=True)

class Update(Resource):
    @swag_from('../yml/update.yml')
    def patch(self, phoneNumber):

        # Get new user information
        args = parser.parse_args()

        # You can use a phone number instead of an ID 
        id = args['id']
        username = args['username']

        message = ""
        # There is no such ID in the table at all 
        if len(User.query.filter_by(id=id).all()) == 0:
            message = make_response(
                jsonify(msg="There is no user with this ID in this database ..."), 404
            )
        # There is no such Username in the table at all 
        elif len(User.query.filter_by(username=username).all()) == 0:
            message = make_response(
                jsonify(msg="There is no user with this Username in this database ..."), 404
            )
        # When there is a ID and username but they are not related
        elif User.query.filter_by(id=id).first().username != username :
            message = make_response(
                jsonify(msg="Username and ID are different ... "), 400
            )
        # This condition applies when the given phone number is in the table
        elif len(User.query.filter_by(phoneNumber=phoneNumber).all()) >= 1:
            message = make_response(
                jsonify(msg="here is a user with this phone number in this database .."), 403
            )
        else :
            # update the information in the database 
            user = User.query.filter_by(id=id, username=username).first()
            user.phoneNumber = phoneNumber
            db.session.commit()
            
            message = make_response(
                jsonify(msg="phone number changed"), 200
            )

        return message






