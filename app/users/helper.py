from datetime import timedelta

from app.models import to_dict, User
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import marshal, abort

db = SQLAlchemy()

def user_post(data):
    username = data.get('username')
    phone = data.get('phone')
    if User.find_by_username(username):
        return abort(422, 'Username  exists')
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
    }

def user_login(data):
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
        }
    else:
        abort(401, 'Password is not correct')

def user_profile(user ,id):
    if type(id)==int:
        raw_data = User.query.filter_by(id=id).first()
    else:
        raw_data = User.query.filter_by(username=id).first()
    user = User.query.filter_by(username=user).first()

    if not raw_data:
        abort(401, "Data can't be found")

    status = 0
    posts = raw_data.posts
    if raw_data.id==user.id:
        status = 2
    elif user.is_subscribing(raw_data):
        status = 1
        posts = [post for post in posts if post.premium==True]
    elif not user.is_subscribing(raw_data):
        posts = [post for post in posts if post.premium==False]

    data = to_dict(raw_data)
    data['subscribing'] = raw_data.subscribed.count()
    data['subscribers'] = raw_data.subscribers.count()
    data['post'] = raw_data.posts.count()
    data['posts'] =posts
    data['status'] = status

    return data

def subscribe(user, target):
    user = User.query.filter_by(username=user).first()
    target = User.query.filter_by(id=int(target)).first()

    if target is None :
        abort(404, 'Target doesn\'t exists')
    elif user is None:
        abort(404, 'User doesn\'t exists')

    if not user.is_subscribing(target):
        user.subscribe(target)
        return {'status': 'You\'re subscribing {} now'.format(target.name),
                'name': user.username,
                'target': target.username
               }
    elif user.is_subscribing(target):
        return {'status': 'You have subscribe this user.',
                'name': user.username,
                'target': target.username
               }
    else:
        abort(500, 'Server Error')

def unsubscribe(user, target):
    user = User.query.filter_by(username=user).first()
    target = User.query.filter_by(id=int(target)).first()

    if target is None :
        abort(404, 'Target doesn\'t exists')
    elif user is None:
        abort(404, 'User doesn\'t exists')

    if not user.is_subscribing(target):
        return {'status': 'You\'re not subscribing this user.',
                'name': user.username,
                'target': target.username
               }
    elif user.is_subscribing(target):
        user.unsubscribe(target)
        return {'status': 'You have unsubscribe this user.',
                'name': user.username,
                'target': target.username
               }
    else:
        abort(500, 'Server Error')

# Check if the the requester asking his own page
def isTheSamePerson(id, username):
    user = User.query.filter_by(id=id).first().username

    return user==username

# Get all subbed user premium posts
def subbed_user(username):
    users = User.query.filter_by(username=username).first()
    subbed_user = users.subscribed
    subs = [i for i in subbed_user]

    if users is None:
        abort(404, 'Data not found')

    if subbed_user is None:
        abort(400, 'No data')

    return subs
