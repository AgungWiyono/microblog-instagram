import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class config(object):
    SQLALCHEMY_DATABASE_URI='postgresql://myuser:password@postgres:5432/flask001'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='guess that'
    MAX_CONTENT_LENGTH=20*1024*1024
    JWT_BLACKLIST_ENABLED=True
    JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh']

    THUMBNAIL_FOLDER='{}/media/thumb/'.format(BASE_DIR)
    HD_FOLDER='{}/media/hd/'.format(BASE_DIR)
    MEDIA_FOLDER='{}/media/'.format(BASE_DIR)
    PROPAGATE_EXCEPTIONS=True

    ERROR_INCLUDE_MESSAGE = False
