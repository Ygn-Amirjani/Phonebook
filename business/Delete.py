from flask import jsonify
from flask_restful import Resource, reqparse, abort
from models.User import User

from db import db

# Delete API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('phoneNumber', type=str, required=True)
parser.add_argument('username', type=str, required=True)

class Delete(Resource):
    def delete(self):
        """ Use DELETE when you want to remove a child resource from the resource collection. """

        # Get new user information
        args = parser.parse_args()

        # You can also use a phone number instead of an ID to remove the user 
        phoneNumber = args['phoneNumber']
        username = args['username']

        # When the desired user was not found 
        self.abort_if_phonenumber_doesnt_exist(phoneNumber, username)

        # remove the information in the database 
        user = User.query.filter_by(phoneNumber=phoneNumber, username=username).first()
        db.session.delete(user)
        db.session.commit()

        return jsonify({"User Deleted": username})

    def abort_if_phonenumber_doesnt_exist(self, phoneNumber, username):
        """ The flask abort method either accepts an error code or it can accept a Response object. """
        
        if len(User.query.filter_by(phoneNumber=phoneNumber).all()) == 0 or \
           len(User.query.filter_by(username=username).all()) == 0 :
            abort(404,message="There is no user with this phone number or username in this database ... ")