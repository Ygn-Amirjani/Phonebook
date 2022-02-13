""" Data models """

from db import db

class User(db.Model):
    """ Data model for user phonebook. """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(13), unique=True, nullable=False)
    username = db.Column(db.String(48), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username