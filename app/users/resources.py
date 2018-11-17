import datetime

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity,\
                                get_raw_jwt, create_access_token, create_refresh_token

from app.users import api
from app.users.helper import userList, userPost, userLogin
from app.users.models import User, RevokedToken
from app.users.serializers import userSchema, userLoginSchema, tesSecretResource
from app.users.serializers import refreshToken


authorization = api.parser()
authorization.add_argument('Authorization', location='headers')
# authorization.add_argument('images', location='files', type='FileStorage')

# for routes that needs authentication of model and header:
# @api.doc(parser = authorization, body=userLoginSchema)

@api.route('/')
@api.doc('show and list users')
class UserList(Resource):
    @api.marshal_list_with(userSchema, envelope='resource', )
    def get(self):
        return userList()

    @api.expect(userSchema, )
    def post(self):
        data = request.get_json()
        status = userPost(data)
        if status == 1:
            return {
                'message' : 'User {} was created.'.format(data['username']),
                'access_token' : create_access_token,
                'refresh_token' : create_refresh_token
            }
        return {'message' : 'Operation failed.\nUser already exists.'}


@api.route('/login')
class UserLogin(Resource):
    @api.expect(userLoginSchema)
    def post(self):
        data = request.get_json()
        status = userLogin(data)
        return status

@api.route('/me')
class SecretResource(Resource):
    @jwt_required
    @api.expect(authorization)
    def get(self):
        me = get_jwt_identity()
        me_id = User.query.filter_by(username=me).first()
        return {'message' : 'hello'}

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
            return {'message' : 'Token has been revoked'}
        except:
            return {'message' : 'Something error'}, 500

@api.route('/logoutRefresh')
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    @api.expect(authorization)
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message' : 'Token has been revoked'}
        except:
            return {'message' : 'Something error'}, 500
