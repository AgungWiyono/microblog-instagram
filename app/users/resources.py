import datetime

from flask import request, redirect, url_for
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity,\
                                get_raw_jwt, create_access_token, create_refresh_token

from app.users import api
from app.users.helper import userPost, userLogin, getMyProfile, userSubscribe
from app.users.helper import otherUserProfile, isTheSamePerson, subbedUser
from app.users.models import User, RevokedToken
from app.users.serializers import userSchema, userLoginSchema
from app.users.serializers import refreshToken, myProfile, userId

authorization = api.parser()
authorization.add_argument('Authorization', location='headers')
# authorization.add_argument('images', location='files', type='FileStorage')

# for routes that needs authentication of model and header:
# @api.doc(parser = authorization, body=userLoginSchema)

@api.route('/')
@api.doc(description='Show logged in user profile')
class UserList(Resource):
    @jwt_required
    @api.expect(authorization)
    @api.marshal_with(myProfile)
    def get(self):
        # Should get the user post and bio
        me = get_jwt_identity()

        # Get user's profile from helper
        data = getMyProfile(me)
        return data

@api.route('/<int:id>')
@api.doc(description='Show user profile with id x')
class OtherUserList(Resource):
    @jwt_required
    @api.expect(authorization)
    def get(self, id):

        # if isTheSamePerson(id, get_jwt_identity()):
        #     return redirect(url_for('user_user_list'))

        data = otherUserProfile(id)

        return data

@api.route('/subsribe')
class Subscribe(Resource):
    @jwt_required
    @api.doc(parser=authorization, body=userId)
    def post(self):
        user = get_jwt_identity()
        target = request.get_json()['user_id']
        target = int(target)

        data = userSubscribe(user, target)
        return data

@api.route('/subbed')
class SubbedUser(Resource):
    @jwt_required
    @api.doc(parser=authorization)
    def get(self):
        username = get_jwt_identity()
        data = subbedUser(username)
        return data

@api.route('/register')
@api.doc(description='user registration')
class UserRegister(Resource):
    @api.expect(userSchema, )
    def post(self):
        data = request.get_json()
        status = userPost(data)
        return status

@api.route('/login')
class UserLogin(Resource):
    @api.expect(userLoginSchema)
    def post(self):
        data = request.get_json()
        status = userLogin(data)
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
