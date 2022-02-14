""" Data models """

from flask import jsonify
from db import db

class User(db.Model):
    """ Data model for user phonebook -> create table and column """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(13), unique=True, nullable=False)
    username = db.Column(db.String(48), nullable=False)

    def __repr__(self):
        return jsonify({'User': self.username})