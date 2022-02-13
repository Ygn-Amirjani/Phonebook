from flask import jsonify
from flask_restful import Resource
from models.User import User

class Select(Resource) :
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        User_found = {'Username': user.username, 'Phonenumber': user.phoneNumber}

        return jsonify(User_found)
