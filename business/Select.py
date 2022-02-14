from flask import jsonify
from flask_restful import Resource
from models.User import User

class Select(Resource) :
    def get(self, username):
        """ Return all users who have this name  """

        User_found = dict()
        for i in range(len(User.query.filter_by(username=username).all())):
            #  We used 'for' because there may be several users with the same name 
            user = User.query.filter_by(username=username).all()[i]
            #  append users to this dictionary
            User_found.update({f'{i}-{user.username}': user.phoneNumber})

        return jsonify(User_found)