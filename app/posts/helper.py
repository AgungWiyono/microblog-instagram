import os
import copy
from datetime import datetime

from PIL import Image
from werkzeug import secure_filename
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

from app.posts.models import Post
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

def toThumbnail(image):
    # Insert resize script here

    # End of resize script

    return image

def checkSize(image):
    pass
    # Script for checking image size

    # Return bool
    # False if image is too big

def saveImageTest(user, hd_folder, thumb_folder, image):
    user = str(User.query.filter_by(username=user).first().id)

    # Rename image filename and create folder
    img_extension = os.path.splitext(image.filename)[1]
    img_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + img_extension

    # Resize and save to HD
    hd_image = Image.open(image)
    hd_path = hd_folder + user + '/' + img_name
    hd_image.save(hd_path)

    # Resize and save to Thumb
    thumbnail_image = Image.open(hd_path)
    thumbnail_image.thumbnail((128,128))
    thumb_path = thumb_folder + user + '/' + img_name
    thumbnail_image.save(thumb_path)


    return user, img_name

def insertPost(data):
    data = Post(
        user_id = data['user_id'],
        story = data['story'],
        uploaded = datetime.utcnow(),
        image = data['image'],
        premium = data['premium'],
        latitude = data['latitude'],
        longitude = data['longitude']
    )

    db.session.add(data)
    db.session.commit()
    return {
        'msg': 'New Arts has been created.'
    }, 201

def showPost(id):
    db_data = Post.query.filter_by(id=id).first()
    data = {}
    data['id'] = db_data.id
    data['story'] = db_data.story
    data['uploaded'] = db_data.uploaded
    data['hd'] = db_data.image
    data['thumb'] = db_data.image
    data['premium'] = db_data.premium
    data['latitude'] = db_data.latitude
