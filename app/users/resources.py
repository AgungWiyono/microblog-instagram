import datetime

from flask import request, redirect, url_for
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity,\
                                get_raw_jwt, create_access_token, create_refresh_token

from app.users import api
from app.users import helper as h
from app.models import User, RevokedToken
from app.users import serializers as s

authorization = api.parser()
authorization.add_argument('Authorization', location='headers')
# authorization.add_argument('images', location='files', type='FileStorage')

# for routes that needs authentication of model and header:
# @api.doc(parser = authorization, body=userLoginSchema)

@api.route('')
@api.doc(description='Show logged in user profile')
class myList(Resource):
    @jwt_required
    @api.expect(authorization)
    @api.marshal_with(s.user_profile)
    def get(self):
        # Should get the user post and bio
        me = get_jwt_identity()

        # Get user's profile from helper
        data = h.user_profile(me, me)
        return data, 200

@api.route('/<int:id>')
@api.doc(description='Show user profile with id x')
class userProfile(Resource):
    @jwt_required
    @api.expect(authorization)
    @api.marshal_with(s.user_profile)
    def get(self, id):
        user = get_jwt_identity()
        data = h.user_profile(user, id)
        return data

@api.route('/subsribe')
class Subscribe(Resource):
    @jwt_required
    @api.doc(parser=authorization, body= s.user_id)
    @api.marshal_with(s.subs_response)
    def post(self):
        user = get_jwt_identity()
        target = request.get_json()['user_id']
        target = int(target)

        data = h.subscribe(user, target)
        return data

@api.route('/unsubscribe')
class Unsubscribe(Resource):
    @jwt_required
    @api.doc(parser= authorization, body= s.user_id)
    @api.marshal_with(s.subs_response)
    def post(self):
        user = get_jwt_identity()
        target = request.get_json()['user_id']
        target= int(target)

        data = h.unsubscribe(user, target)
        return data

@api.route('/subbed')
class SubbedUser(Resource):
    @jwt_required
    @api.doc(parser=authorization)
    @api.marshal_with(s.mini_profile)
    def get(self):
        username = get_jwt_identity()
        data = h.subbed_user(username)
        return data

@api.route('/register')
@api.doc(description='user registration')
class UserRegister(Resource):
    @api.expect(s.user_schema)
    @api.marshal_with(s.register_response)
    def post(self):
        data = request.get_json()
        status = h.user_post(data)
        return status

@api.route('/login')
class UserLogin(Resource):
    @api.expect(s.user_login)
    @api.marshal_with(s.login_response)
    def post(self):
        data = request.get_json()
        status = h.user_login(data)
        return status

# =======================================================================
@api.route('/refresh_token')
class refreshToken(Resource):
    @jwt_refresh_token_required
    @api.expect(authorization)
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, expires_delta= datetime.timedelta(hours=5))
        return {'access_token' : access_token}


@api.route('/logoutAccess')
class UserLogoutAccess(Resource):
    @jwt_required
    @api.expect(authorization)
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'msg' : 'Token has been revoked'}
        except:
            return {'msg' : 'Something error'}, 500

@api.route('/logoutRefresh')
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    @api.expect(authorization)
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'msg' : 'Token has been revoked'}
        except:
            return {'msg' : 'Something error'}, 500
