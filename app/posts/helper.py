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

def createLocation(user, hd_path, thumb_path, temp_path):
    hd_path = hd_path + user +'/'
    thumb_path = thumb_path + user +'/'
    temp_path = temp_path + user + '/'
    if not os.path.exists(hd_path):
        os.makedirs(hd_path)
    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

def toThumbnail(image):
    # Insert resize script here

    # End of resize script

    return image

def checkSize(image):
    pass
    # Script for checking image size

    # Return bool
    # False if image is too big

def saveImageTest(user, hd_folder, thumb_folder, temp_folder, image):

    # Rename image filename and create folder
    img_extension = os.path.splitext(image.filename)[1]
    img_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + img_extension
    temp_path = temp_folder + user + '/' + img_name
    image.save(temp_path)


    # Resize and save to Thumb
    thumbnail_image = Image.open(temp_path)
    thumbnail_image.thumbnail((128,128))
    thumb_path = thumb_folder + user + '/' + img_name
    thumbnail_image.save(thumb_path)

    # Resize and save to HD
    hd_image = Image.open(temp_path)
    hd_path = hd_folder + user + '/' + img_name
    hd_image.save(hd_path)

    return img_name

def insertPost(data):
    user= User.query.filter_by(username= get_jwt_identity()).first()
    user_id = user.id
    post = data.get('story')
    image = data.get('image')

    data = Post(
        story= post,
        user_id = user_id,
        large = hd,
        thumbnail = thumb,
        uploaded = datetime.utcnow()
    )
    db.session.add(data)
    db.session.commit()

