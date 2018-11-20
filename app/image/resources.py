from app.image import api

from flask import current_app, send_from_directory, request
from flask_restplus import Resource

@api.route('/hd/<id>/<filename>')
class hd_image(Resource):
    def get(self, id, filename):
        hd_folder = current_app.config['HD_FOLDER']

        folder = id
        filename = filename
        comp_path = hd_folder + folder

        return send_from_directory(
            comp_path,
            filename
        )


@api.route('/thumb/<id>/<filename>')
class thumb_image(Resource):
    def get(self, id, filename):
        thumb_folder = current_app.config['THUMBNAIL_FOLDER']

        folder = id
        filename = filename
        thumb_path = thumb_folder + folder

        return send_from_directory(
            thumb_path,
            filename
        )
