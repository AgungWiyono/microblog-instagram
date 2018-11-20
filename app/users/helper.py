from datetime import timedelta

from app import User
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import marshal

from app.users.serializers import *

db = SQLAlchemy()

def userPost(data):
    username = data.get('username')
    phone = data.get('phone')
    if User.find_by_username(username):
        return {
            'msg' : 'Username is exists'
        }, 422
    if User.is_phone_exists(phone):
        return{
            'msg': 'Phone number exist'
        }, 422
    if phone.isalpha():
        return {
            'msg': 'Phone number must contain numbers only.'
        }, 422

    password = User.hash_password(data.get('password'))
    data = User(username=username, password=password, phone=phone, poin=50)
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
            'id': exist_user.id,
            'token' : access_token
        },200
    else:
        return {'msg' : 'Password is not correct.'},401

# Get user's profile
def getMyProfile(name):
    data = User.query.filter_by(username=name).first()

    return data

def userSubscribe(user, target):
    user = User.query.filter_by(username=user).first()
    target = User.query.filter_by(id=int(target)).first()

    if target is None :
        return {'msg': 'target doesnt exist'}, 404
    elif user is None:
        return {'msg': 'user doesnt exist'}, 404

    if not user.is_subscribing(target):
        user.subscribe(target)
        return {'msg': 'You have subscribed now',
                'name': user.username,
                'target': target.username
               }, 200
    elif user.is_subscribing(target):
        user.unsubscribe(target)
        return {'msg': 'Unscribing success',
                'name': user.username,
                'target': target.username
               }, 200
    else:
        return {'msg': 'Server error'}, 500

def otherUserProfile(id):
    raw_data = User.query.filter_by(id=id).first()

    if not raw_data:
        return {'msg': "Data can't be found."}, 404

    data = {}
    data['username'] = raw_data.username
    data['phone'] = raw_data.phone
    data['about'] = raw_data.about
    data['poin'] = raw_data.poin
    data['subscribed'] = raw_data.subscribed.count()
    data['subscribers'] = raw_data.subscribers.count()
    data['posts'] = raw_data.posts[:2]

    return marshal(data, otherUserProfileSch), 200


