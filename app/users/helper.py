from datetime import timedelta

from app import User
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import marshal, abort

from app.users.serializers import *

db = SQLAlchemy()

def userPost(data):
    username = data.get('username')
    phone = data.get('phone')
    if User.find_by_username(username):
        abort(422, 'Username  exists')
    if User.is_phone_exists(phone):
        abort(422, 'Phone number is exists')
    if phone.isalpha():
        abort(422, 'Phone number should contain numbers only')

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
        abort(404, 'User doesn\'t exists')

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
    posts = data.posts[:5]
    data_dict = data.toDict()
    data_dict['posts'] = posts
    data_dict['photo'] = data.id

    return data_dict

def userSubscribe(user, target):
    user = User.query.filter_by(username=user).first()
    target = User.query.filter_by(id=int(target)).first()

    if target is None :
        abort(404, 'Target doesn\'t exists')
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

    data = raw_data.toDict()
    data['subscribing'] = raw_data.subscribed.count()
    data['subscribers'] = raw_data.subscribers.count()
    data['posts'] = raw_data.posts[:2]

    return marshal(data, otherUserProfileSch), 200

# Check if the the requester asking his own page
def isTheSamePerson(id, username):
    user = User.query.filter_by(id=id).first().username

    return user==username

# Get all subbed user premium posts
def subbedUser(username):
    users = User.query.filter_by(username=username).first()
    subbed_user = users.subscribed
    subs = [i for i in subbed_user]

    if users is None:
        return {'msg': 'Data not found'}, 404

    if subbed_user is None:
        return {'msg': 'No Data'}, 400

    return marshal(subs, miniProfileSch), 200

