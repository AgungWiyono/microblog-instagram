from datetime import datetime
import json

from flask import current_app, request, send_from_directory
from flask_restplus import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.posts import api
from app.posts.helper import createLocation, saveImageTest, insertPost
from app.posts.helper import showUserPost
from app.posts.serializers import postInsert, postList

app = current_app

post = api.parser()
post.add_argument('Authorization', location='headers')
post.add_argument('image', location='files', type='FileStorage')
post.add_argument('story', type=str, location='form')
post.add_argument('premium', type=bool, location='form')
post.add_argument('convert', type=bool, location='form')


@api.route('/')
class post(Resource):
    @jwt_required
    @api.doc(parser=post)
    def post(self):
        user = get_jwt_identity()

        thumb_folder = app.config['THUMBNAIL_FOLDER']
        hd_folder = app.config['HD_FOLDER']
        createLocation(user, hd_folder, thumb_folder)

        user_id, new_name = saveImageTest(
                    user,
                    hd_folder,
                    thumb_folder,
                    request.files['image'],
                    )

        premium = True if request.form['premium']=='true'\
                else False
        post_data = {}
        post_data['user_id'] = user_id
        post_data['story'] = request.form['story']
        post_data['premium']= premium
        post_data['image'] = str(user_id) + '/' + new_name

        status = insertPost(post_data)
        return status


@api.route('/<int:id>')
class showPost(Resource):
    def get(self, id):
        data = showUserPost(id)

        if data==0:
            return {'msg': 'Data not found'}, 404
        return marshal(data, postList), 200
