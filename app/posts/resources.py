from flask import current_app, request, send_from_directory
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.posts import api
from app.posts.helper import createLocation, saveImage, insertPost
from app.posts.serializers import postInsert

app = current_app

img = api.parser()
img.add_argument('Authorization', location='headers')
img.add_argument('image', location='files', type='FileStorage')
img.add_argument('post_body', location='form', type='string')

@api.route('/post')
class post(Resource):
    @jwt_required
    @api.doc(parser=img)
    def post(self):
        user = get_jwt_identity()
        hd_folder = app.config['HD_FOLDER']
        thumb_folder = app.config['THUMBNAIL_FOLDER']
        temp_folder = app.config['TEMP_FOLDER']
        createLocation(user, hd_folder, thumb_folder, temp_folder)
        new_name = saveImage(
                    user,
                    hd_folder,
                    thumb_folder,
                    temp_folder,
                    request.files['image'],
                    )

        base_url = request.host_url + 'img' + '/'
        hd_url = base_url + 'hd'
        thumb_url = base_url + 'thumb'
        args = '?username={}&filename={}'.format(user, new_name)

        post_data = {}
        post_data['story'] = request.form['post_body']
        post_data['hd'] = hd_url + args
        post_data['thumb'] = thumb_url + args
        insertPost(post_data)
        return {
            'hd url': hd_url + args,
            'thumb url': thumb_url + args,
            'detail': post_data['story']
        }
