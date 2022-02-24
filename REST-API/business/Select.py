from flask import jsonify, make_response
from flask_restful import Resource
from flasgger import swag_from
import logging

from models.User import User

class Select(Resource) :
    @swag_from('../yml/select.yml')
    def get(self, username):
        """ Return all users who have this name  """

        user_found = dict()
        for i in range(len(User.query.filter_by(username=username).all())):
            #  We used 'for' because there may be several users with the same name 
            user = User.query.filter_by(username=username).all()[i]
            #  append users to this dictionary
            user_found.update({f'{i}-{user.username}': user.phoneNumber})

        logging.basicConfig(filename='/var/log/restapi/app.log', format='%(asctime)s - [%(levelname)s] - %(message)s',  
        datefmt='%d-%b-%y %H:%M:%S')

        message = ""
        # This condition is enforced when the given username does not exist in the table 
        if  len(user_found) == 0 :
            message = make_response(
                jsonify(msg="user not found in this database ."), 404
            )
            logging.error("User Not Found in this database.")
        else:
            message = make_response(
                jsonify(user_found), 200
            )

        return message

