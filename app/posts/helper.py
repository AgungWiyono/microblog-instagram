import os
import copy
from datetime import datetime
import json

from skimage.transform import resize
from skimage.io import imread, imsave

from werkzeug import secure_filename
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import marshal, abort

from app.posts.models import Post
from app.posts.serializers import postFeed, postList
from app.posts.converter import convert
from app import User

db = SQLAlchemy()

def createLocation(user, hd_path, thumb_path):
    user = str(User.query.filter_by(username=user).first().id)
    hd_path = hd_path + user +'/'
    thumb_path = thumb_path + user +'/'
    if not os.path.exists(hd_path):
        os.makedirs(hd_path)
    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)

def checkSize(image):
    pass
    # Script for checking image size

    # Return bool
    # False if image is too big

def saveImageTest(user, hd_folder, thumb_folder, image, is_convert):
    user = str(User.query.filter_by(username=user).first().id)

    # Rename image filename and create folder
    img_extension = os.path.splitext(image.filename)[1]
    img_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + img_extension

    if is_convert=='true':
        image = convert(image)
    else:
        image = imread(image)

    # Resize and save to HD
    hd_image = image
    hd_path = hd_folder + user + '/' + img_name
    imsave(hd_path, hd_image)

    # Resize and save to Thumb
    thumbnail_image = imread(hd_path)
    thumbnail_image = resize(thumbnail_image, (128,128))
    thumb_path = thumb_folder + user + '/' + img_name
    imsave(thumb_path, thumbnail_image)


    return user, img_name

def insertPost(data):
    data = Post(
        user_id = data['user_id'],
        story = data['story'],
        uploaded = datetime.utcnow(),
        image = data['image'],
        premium = data['premium'],
    )

    db.session.add(data)
    db.session.commit()
    return {
        'msg': 'New Arts has been created.'
    }, 201

def showUserPost(id):
    db_data = Post.query.filter_by(id=id).first()

    if db_data is None:
        print('go to abort')
        abort(404, 'Post not found')
    return db_data, 200

# Getting non=premium post for explore endpoint
def explorePost():
    posts = Post.query.filter_by(premium=False).order_by(Post.uploaded.desc()).limit(10).all()

    return marshal(posts, postFeed), 200
