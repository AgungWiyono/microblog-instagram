import os.path

from flask import current_app, send_from_directory, request, send_file
from flask_restplus import Resource

from app.image import api

@api.route('/hd/<id>/<filename>')
class hd_image(Resource):
    def get(self, id, filename):
        hd_folder = current_app.config['HD_FOLDER']

        comp_path = hd_folder + id + '/'
        fullpath = comp_path + filename

        if not os.path.isfile(fullpath):
            # return {'msg': 'File not found.\nIt could be deleted.'}, 404
            return {'msg': fullpath}, 404

        return send_file(str(fullpath))


@api.route('/thumb/<id>/<filename>')
class thumb_image(Resource):
    def get(self, id, filename):
        thumb_folder = current_app.config['THUMBNAIL_FOLDER']

        thumb_path = thumb_folder + id + '/'
        fullpath = thumb_path+  filename

        if not os.path.isfile(fullpath):
            # return {'msg': 'File not found.\nIt could be deleted.'}, 404
            return {'msg': fullpath}, 404

        return send_file(str(fullpath))

@api.route('/<int:id>')
class profile_image(Resource):
    def get(self, id):
        base = current_app.config['MEDIA_FOLDER']
        fullpath = base+'{}/profile.jpg'.format(id)

        if not os.path.isfile(fullpath):
            fullpath=base+'default/profile.jpg'
            return send_file(fullpath)
        else:
            return fullpath
