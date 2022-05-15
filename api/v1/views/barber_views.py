from api.v1 import db
from api.v1.views import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style
from flask import jsonify, make_response, request, abort


@app_views.route('/user/barber/', methods=['POST'])
def create_barber():
    """ Creates a new barber.

    Return: A dictionary representation on the instance of the new barber.
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    compulsory_data = ['id', 'username', 'password', 'email', 'country', 'state',
                       'city', 'address']
    for attr in compulsory_data:
        if attr not in data:
            return make_response(jsonify({'error': 'Missing ' + attr}), 400)

    barber = Barber(**data)
    db.session.add(barber)
    db.session.commit()

    return make_response(jsonify(barber.to_dict()), 201)


@app_views.route('/user/barber/activate/<barber_id>', methods=['PUT'])
def activate_barber(barber_id):
    """
        This function activates a barber's account
    :return:
    """
    barber = Barber.query.filter_by(id=barber_id).first()
    if barber is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for k, v in request.get_json().items():
        setattr(barber, k, v)

    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


@app_views.route('/user/barbers/', methods=['GET'])
def get_barbers():
    """Gets user information for all barbers."""
    barbers = []
    for barber in Barber.query.all():
        barbers.append(barber.to_dict())

    return jsonify(barbers)


@app_views.route('/user/barber/<barber_id>', methods=['GET'])
def get_a_barber(barber_id):
    """Gets a particular barber by it's id
    Args:
        barber_id (int): Unique id of a barber.
    
    Returns information of a barber.
    """
    barber = Barber.query.filter_by(id=barber_id).first()
    if barber is None:
        abort(404)
    return jsonify(barber.to_dict())


@app_views.route('/user/barber/<barber_id>', methods=['PUT'])
def edit_barber(barber_id):
    """Updates a barber.
    Args:
        barber_id (int): Unique id of a barber.
    """
    barber = Barber.query.filter_by(id=barber_id).first()
    if barber is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for k, v in request.get_json().items():
        setattr(barber, k, v)

    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


@app_views.route('/user/barber/<barber_id>', methods=['DELETE'])
def delete_a_barber(barber_id):
    """ Deletes a barber.
    Args:
        barber_id (int): Unique id of a barber.
    """
    barber = Barber.query.filter_by(id=barber_id).first()
    if barber is None:
        abort(404)

    db.session.delete(barber)
    db.session.commit()
    del barber
    return jsonify({})


@app_views.route('/user/barbers/<string:location>', methods=['GET'])
def get_barbers_by_location(location):
    """ Returns all barbers that exactly or closely match the location
    data passed in json.

    :return:
    """
    pass


@app_views.route('/create_style', methods=['POST'])
def create_new_style():
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


@app_views.route('/barber/<barber_id>/add_style', methods=['PUT'])
def select_styles(barber_id):
    """ Adds styles to a barbers list of styles.
    
    Args:
        barber_id (int): Unique id for a barber.
    
    Return: List of barber's styles.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data = request.get_json()
    if 'id' not in data:
        return make_response(jsonify({'error': 'Missing style id'}), 400)

    barber = Barber.query.filter_by(id=barber_id).first()
    style = Style.query.filter_by(id=data['id']).first()
    if barber is None or style is None:
        abort(404)

    barber.styles.append(style)
    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


@app_views.route('/barber/<barber_id>/remove_style', methods=['PUT'])
def unselect_a_styles(barber_id):
    """ Removes a style from the list of a barber's styles
    
    Args:
        barber_id (int): Unique id for a barber.
    
    Return: List of barber's styles.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data = request.get_json()
    if 'id' not in data:
        return make_response(jsonify({'error': 'Missing style id'}), 400)

    barber = Barber.query.filter_by(id=barber_id).first()
    style = Style.query.filter_by(id=data['id']).first()
    if barber is None or style is None:
        abort(404)

    barber.styles.remove(style)
    db.session.add(barber)
    db.session.commit()

    return jsonify(barber.to_dict())
