from datetime import timedelta

from app.users.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token

db = SQLAlchemy()

def userList():
    data = User.query.all()
    return data

def userRegister(data):
    username = data.get('username')
    phone = data.get('phone')
    pwd = data.get('password')
    photo = data.get('photo')

    if username is None or phone is None or pwd is None:
        return {
            'msg': 'Please fill all fields.'
        }, 422


    if User.find_by_username(username):
        return {
            'msg' : 'Username is exists'
        }, 422
    if User.is_phone_exists(phone):
        return{
            'msg': 'Phone number exist'
        }, 422

    password = User.hash_password(data.get('password'))
    data = User(username=username, password=password, phone=phone, photo=photo)

    db.session.add(data)
    db.session.commit()
    return {
        'username': username,
        'phone': phone,
        'token': create_access_token(identity=username)
    },200

def userLogin(data):
    username = data.get('username')
    password = data.get('password')

    exist_user = User.query.filter_by(username=username).first()
    if not exist_user:
        return {'msg' : "User doesn't exists."},404

    if User.verify_password(password, exist_user.password):
        access_token = create_access_token(identity=data['username'], expires_delta=timedelta(hours=10))
        refresh_token = create_refresh_token(identity=data['username'])

        return {
            'username': exist_user.username ,
            'user_id': exist_user.id,
            'token' : access_token
        },200
    else:
        return {'msg' : 'Password is not correct.'},401

# Get user's profile
def getMyProfile(name):
    data = User.query.filter_by(username=name).first()

    '''
    if data is None:
        return {'msg' : 'User not found.'}, 404
    '''
    return data

