from email import message
from flask import jsonify
from flask_restful import Resource, abort
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

        # When there is no user, our dictionary does not hold any value. 
        self.abort_if_username_doesnt_exist(user_found=user_found)
        
        return jsonify(user_found)

    def abort_if_username_doesnt_exist(self, user_found):
        """ The flask abort method either accepts an error code or it can accept a Response object. """
        if  len(user_found) == 0 :
            abort(404,message="User Not Fount ...")

