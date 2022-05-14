# from .v1 import app_views
# from api.v1 import app_views
from api.v1.app import db
from api.v1.views import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style
from flask import jsonify, make_response, request, abort


@app_views.route('/')
def index():
    """
        Test view point to ensure that the endpoint is connecting
    :return:
    """
    return 'Hello Africa!'


@app_views.route('/user/cust/', methods=['POST'])
def create_a_cust():
    """Creates a new customer."""
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr in ['id', 'email']:
        if attr not in data:
            return make_response(jsonify({'error': 'Missing ' + attr}), 400)

    cust = User(**data)
    db.session.add(cust)
    db.session.commit()

    return make_response(jsonify(cust.to_dict()), 201)


@app_views.route('/user/customers/', methods=['GET'])
def get_custs():
    """Gets all customers."""
    custs = []
    for cust in User.query.all():
        cust.append(cust.to_dict())

    return jsonify(custs)


@app_views.route('/user/cust/<cust_id>', methods=['GET'])
def get_a_cust(cust_id):
    """Get a customer.

    Args:
        cust_id (int): Unique customer id.
    
    Return: Information of the customer that owns the given id.
    """
    cust = User.query.filter_by(id=cust_id).first()
    if cust is None:
        abort(404)
    return jsonify(cust.to_dict())


@app_views.route('/user/cust/<cust_id>', methods=['PUT'])
def edit_a_cust(cust_id):
    """Updates a customer.

     Args:
        cust_id (int): Unique customer id.

    Return: Information of the customer that owns the given id.
    """
    cust = User.query.filter_by(id=cust_id).first()
    if cust is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for k, v in request.get_json().items():
        setattr(cust, k, v)

    db.session.add(cust)
    db.session.commit()
    return jsonify(cust.to_dict())



@app_views.route('/user/cust/<cust_id>', methods=['DELETE'])
def delete_a_cust():
    """Deletes a customer.
    
    Args:
        cust_id (int): Unique id of a customer.
    """
    cust = User.query.filter_by(id=cust_id).first()
    if cust is None:
        abort(404)

    db.session.delete(cust)
    db.session.commit()
    del cust
    return (jsonify({}))
