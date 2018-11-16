from datetime import timedelta

from app.users.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token

db = SQLAlchemy()

def userList():
    data = User.query.all()
    return data

def userPost(data):
    username = data.get('username')
    if User.find_by_username(username):
        return 0

    password = User.hash_password(data.get('password'))
    phone = data.get('phone')
    data = User(username=username, password=password, phone=phone)
    db.session.add(data)
    db.session.commit()
    return 1

def userLogin(data):
    username = data.get('username')
    password = data.get('password')

    exist_user = User.query.filter_by(username=username).first()
    if not exist_user:
        return ({'message' : "User doesn't exists."})

    if User.verify_password(password, exist_user.password):
        access_token = create_access_token(identity=data['username'], expires_delta=timedelta(hours=10)),
        refresh_token = create_refresh_token(identity=data['username'])

        return {
            'message' : 'Logged in as {}'.format(data['username']),
            'access_token' : access_token,
            'refresh_token' : refresh_token
        }
    else:
        return {'message' : 'Login failed.'}