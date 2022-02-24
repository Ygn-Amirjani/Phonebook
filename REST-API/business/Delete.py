from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
import sqlalchemy, logging

from models.User import User
from db import db

# Delete API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('phoneNumber', type=str, required=True)
parser.add_argument('username', type=str, required=True)

message = ""

class Delete(Resource):
    @swag_from('../yml/delete.yml')
    def delete(self):
        """ Use DELETE when you want to remove a child resource from the resource collection. """

        # Get new user information
        args = parser.parse_args()

        # You can also use a phone number instead of an ID to remove the user 
        phoneNumber = args['phoneNumber']
        username = args['username']

        logging.basicConfig(filename='/var/log/restapi/app.log', format='%(asctime)s - [%(levelname)s] - %(message)s',  
        datefmt='%d-%b-%y %H:%M:%S')
        
        # remove the information in the database 
        try:
            user = User.query.filter_by(phoneNumber=phoneNumber, username=username).first()
            db.session.delete(user)
            db.session.commit()
            message = make_response(
                jsonify(msg="User Deleted"), 200
            )
        except sqlalchemy.exc.InvalidRequestError as e:
            message = make_response(
                jsonify(msg="I could not perform the desired operation. Please check the information and try again :)"), 400
            )
            logging.error(e)

        return message