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

        # When the program fails 
        self.abort_if_phonenumber_doesnt_exist(phoneNumber, username)

        # remove the information in the database 
        user = User.query.filter_by(phoneNumber=phoneNumber, username=username).first()
        db.session.delete(user)
        db.session.commit()

        return jsonify({"User Deleted": username})

    def abort_if_phonenumber_doesnt_exist(self, phoneNumber, username):
        """ The flask abort method either accepts an error code or it can accept a Response object. """

        # There is no such phone number in the table at all 
        if len(User.query.filter_by(phoneNumber=phoneNumber).all()) == 0 :
            abort(404,message="There is no user with this phone number in this database ... ")
        # There is no such username in the table at all 
        elif len(User.query.filter_by(username=username).all()) == 0:
            abort(404,message="There is no user with this username in this database ... ")
        # When there is a phone number and username but they are not related
        elif User.query.filter_by(phoneNumber=phoneNumber).first().username != username :
            abort(404,message="Username and phone number are different ... ")
