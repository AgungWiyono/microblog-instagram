from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api, Resource
from flask_jwt_extended import JWTManager

from config import config as Cof


#importing api resources

db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app(config=Cof):
    app = Flask(__name__)
    app.config.from_object(config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app, title='My Test')


    return app



from .posts.models import Post
from .users.models import User, RevokedToken

from .users.resources import api as userApi
from .posts.resources import api as postApi

api.add_namespace(userApi, path='/users')
api.add_namespace(postApi, path='/posts')

from .image.resources import api as imageApi
api.add_namespace(imageApi, path='/media')


jwt._set_error_handler_callbacks(api)

@jwt.token_in_blacklist_loader
def check_is_token_blacklisted(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)

@jwt.expired_token_loader
def expired_token():
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': 'The token has expired'
    }), 401
