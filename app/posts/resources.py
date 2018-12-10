from datetime import datetime
import json

from flask import current_app, request, send_from_directory
from flask_restplus import Resource, marshal, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.posts import api
from app.posts import helper as h
from app.posts import serializers as s

app = current_app

post = api.parser()
post.add_argument('Authorization', location='headers')
post.add_argument('image', location='files', type='FileStorage')
post.add_argument('story', type=str, location='form')
post.add_argument('premium', type=bool, location='form')
post.add_argument('convert', type=bool, location='form')


@api.route('')
class post(Resource):
    @jwt_required
    @api.doc(parser=post)
    @api.marshal_with(s.post_insert)
    def post(self):
        user = get_jwt_identity()

        thumb_folder = app.config['THUMBNAIL_FOLDER']
        hd_folder = app.config['HD_FOLDER']
        h.create_location(user, hd_folder, thumb_folder)

        print(request.form)

        user_id, new_name = h.save_image(
                    user,
                    hd_folder,
                    thumb_folder,
                    request.files['image'],
                    request.form['convert']
                    )

        premium = True if request.form['premium']=='true'\
                else False
        post_data = {}
        post_data['user_id'] = user_id
        post_data['story'] = request.form['story']
        post_data['premium']= premium
        post_data['image'] = str(user_id) + '/' + new_name

        status = h.insert_post(post_data)
        return status


@api.route('/<int:id>')
class showPost(Resource):
    @api.marshal_with(s.post_list)
    def get(self, id):
        data = h.show_user_post(id)

        return data

@api.route('/explore')
class explore(Resource):
    @api.marshal_with(s.post_feed)
    def get(self):
        data = h.explore_post()
        return data
