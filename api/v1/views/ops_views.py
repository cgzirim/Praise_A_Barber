from . import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style
from flask import request, make_response, jsonify, abort
from api.v1.app import db


@app_views.route('/barber/rate', methods=['POST'])
def rate_a_barber():
    pass


@app_views.route('/style/create', methods=['POST'])
def add_styles():
    """Creates a new style.

    Return: Information on new style.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data = request.get_json()
    if 'id' not in data:
        return make_response(jsonify({'error': 'Missing id'}), 400)
    if Style.query.filter_by(id=data['id']).first():
        return make_response(jsonify({'error': 'Existing id'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if 'image' not in data:
        return make_response(jsonify({'error': 'Missing image URI'}), 400)

    style = Style(**data)
    db.session.add(style)
    db.session.commit()

    style_info = {
            'id': style.id,
            'name': style.name,
            'image': style.image,
            'description': style.description
            }
    return make_response(jsonify(style_info), 201)


@app_views.route('/style/<style_id>/remove', methods=['DELETE'])
def remove_styles(style_id):
    """
        This function will enable an admin remove styles from the database
    :return:
    """
    style = Style.query.filter_by(id=style_id).first()
    if style is None:
        abort(404)

    db.session.delete(style)
    db.session.commit()
    del style
    return jsonify({})
