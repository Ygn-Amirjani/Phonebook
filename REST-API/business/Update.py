from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
import logging

from models.User import User
from db import db

# Update API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id', type=int, required=True)
parser.add_argument('username', type=str, required=True)

message = ""

class Update(Resource):
    @swag_from('../yml/update.yml')
    def patch(self, phoneNumber):

        # Get new user information
        args = parser.parse_args()

        # You can use a phone number instead of an ID 
        id = args['id']
        username = args['username']

        logging.basicConfig(filename='/var/log/restapi/app.log', format='%(asctime)s - [%(levelname)s] - %(message)s',  
        datefmt='%d-%b-%y %H:%M:%S')

        # update the information in the database 
        try:
            user = User.query.filter_by(id=id, username=username).first()
            user.phoneNumber = phoneNumber
            db.session.commit()
            message = make_response(
                jsonify(msg="phone number changed"), 200
            )
        except Exception as e:
            message = make_response(
                jsonify(msg="I could not perform the desired operation. Please check the information and try again :)"), 400
            )
            logging.error(e)

        return message






