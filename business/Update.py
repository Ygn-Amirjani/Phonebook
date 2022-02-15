from flask import jsonify
from flask_restful import Resource, reqparse, abort
from models.User import User

from db import db

# Update API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id', type=int, required=True)
parser.add_argument('username', type=str, required=True)

class Update(Resource):
    def patch(self, phoneNumber):

        # Get new user information
        args = parser.parse_args()

        # You can use a phone number instead of an ID 
        id = args['id']
        username = args['username']

        # When the program fails 
        self.abort_if_user_doesnt_exist(id,phoneNumber, username)

        # update the information in the database 
        user = User.query.filter_by(id=id, username=username).first()
        user.phoneNumber = phoneNumber
        db.session.commit()

        return jsonify({"Your phone number changed to this ": phoneNumber})

    def abort_if_user_doesnt_exist(self,id,phoneNumber, username):
        """ The flask abort method either accepts an error code or it can accept a Response object. """

        # There is no such ID in the table at all 
        if len(User.query.filter_by(id=id).all()) == 0:
            abort(404, message="There is no user with this ID in this database ...")
        # There is no such Username in the table at all 
        elif len(User.query.filter_by(username=username).all()) == 0:
            abort(404, message="There is no user with this Username in this database ...")
        # When there is a ID and username but they are not related
        elif User.query.filter_by(id=id).first().username != username :
            abort(404,message="Username and ID are different ... ")
        # This condition applies when the given phone number is in the table
        elif len(User.query.filter_by(phoneNumber=phoneNumber).all()) >= 1:
            abort(404, message="here is a user with this phone number in this database ...")






