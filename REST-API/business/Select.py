from flask import jsonify, make_response
from flask_restful import Resource
from models.User import User

class Select(Resource) :
    def get(self, username):
        """ Return all users who have this name  """

        user_found = dict()
        for i in range(len(User.query.filter_by(username=username).all())):
            #  We used 'for' because there may be several users with the same name 
            user = User.query.filter_by(username=username).all()[i]
            #  append users to this dictionary
            user_found.update({f'{i}-{user.username}': user.phoneNumber})

        message = ""
        # This condition is enforced when the given username does not exist in the table 
        if  len(user_found) == 0 :
            message = make_response(
                jsonify(msg="There is no user with this name ..."), 400
            )
        else:
            message = make_response(
                jsonify(user_found), 200
            )

        return message

