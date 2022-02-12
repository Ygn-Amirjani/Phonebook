from config import Config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return jsonify("Just For Check :) ")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()