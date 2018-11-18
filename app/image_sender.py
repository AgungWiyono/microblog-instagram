from flask import Blueprint, request, send_from_directory
from flask import current_app as app
from app import User

img_sender = Blueprint('image_sender', __name__, url_prefix='/img')

@img_sender.route('/hd', methods=['GET'])
def send_hd():
    name = request.args.get('username')
    filename = request.args.get('filename')
    user_id = str(User.get_user_id(name))

    user_dir = app.config['HD_FOLDER'] + user_id + '/'
    return send_from_directory(
        user_dir,
        filename
    )


@img_sender.route('/thumb', methods=['GET'])
def send_thumb():
    name = request.args.get('username')
    filename = request.args.get('filename')
    user_id = str(User.get_user_id(name))

    user_dir = app.config['THUMBNAIL_FOLDER'] + user_id + '/'
    return send_from_directory(
        user_dir,
        filename
    )

@img_sender.route('/def_photo', methods=['GET'])
def default_photo():
    return send_from_directory(
        app.config['DEFAULT_FOLDER'],
        'photo.png'
    )

