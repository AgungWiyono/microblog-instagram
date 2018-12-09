from flask import Blueprint, jsonify, make_response

bp = Blueprint('error', __name__)

@bp.errorhandler(404)
def not_found():
    print('this is error')
    return make_response(jsonify({'msg': 'get'}))
