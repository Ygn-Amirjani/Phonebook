# [RESTFUL API](https://github.com/flask-restful/flask-restful)

In this project, we tried to make a phone book with ‍‍‍‍‍‍‍`‍RestFul‍` standards .

You can save your contacts, change the contact number you want, delete that contact, and return number if needed .

We also use Swagger to document Api for convenience And that's it :) now you can open http://localhost:8000/apidocs to see available APIs.

### Development Environment (using Docker)

First you need to download [docker](https://docs.docker.com/engine/install/ubuntu/) 
and [docker-compose](https://docs.docker.com/compose/install/).

then run the following command :

```
docker-compose up
```

### Development Environment (Without Docker)

You must first set up a virtual environment :

```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

Download the required packages :

```
python -m pip install -r requirements.txt
```

Then you can run :

```
cd REST-API 
python app.py
```

### Database Connection

This project supports `MySql` as its database. 

To connect the code to your database. change `username`, `password` and `db` in `config.json` to make the app able to connect
to database. and And create the conf.json file path in the flaskConfig function .

You can use the following command to install MySql (MariaDb Because it is an open source) :

```
sudo apt install mariadb-server
sudo systemctl start mariadb.service 
```

To create the user :

```
sudo mysql
CREATE USER 'Username'@'localhost' IDENTIFIED BY 'Password';
GRANT ALL PRIVILEGES ON *.* TO 'database_user'@'localhost';
```

### Links that can be used to better understand 

For more information read this:

* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

