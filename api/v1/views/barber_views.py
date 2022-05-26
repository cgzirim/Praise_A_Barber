from api.v1 import db, app
from api.v1.views import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style
from flask import jsonify, make_response, request, abort
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import jwt


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'You need to be logged in'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Barber.query.filter_by(id=data['id']).first()

        except Exception as e:
            print(f'{e.__class__} - {str(e)} - {e}')
            return jsonify({
                'message': 'Login Invalid'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app_views.route('/json/login', methods=['POST'])
def loginWithJson():
    """
        This is the login function, data will be collected with json
    :return: jwt token
    """
    # creates dictionary of form data
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(jsonify({'message': 'Could not verify'}), 401)

    user = Barber.query.filter_by(username=auth.get('username')).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(jsonify({'message': 'User not found'}), 401)

    print('passed user check')
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(jsonify({'message': 'password incorrect'}), 403)


@app_views.route('/login', methods=['POST'])
def login():
    """
        This is the login function, data will be collected with form-data
    :return: jwt token
    """
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = Barber.query.filter_by(username=auth.get('username')).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'user not found',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )
    print('passed user check')
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app_views.route('/logout')
def logout():
    """ function to handle user logout by expiring session token"""
    pass


@app_views.route('/dashboard')
@login_required
def dashboard(current_user):
    """Dashboard view"""
    print(current_user)
    return jsonify({'message': 'You have access to the dashboard'}), 200


# Create a barber
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

    data['id'] = str(uuid.uuid4())
    data['password'] = generate_password_hash(data['password'])
    barber = Barber(**data)
    db.session.add(barber)
    db.session.commit()
    print(barber.to_dict())
    return jsonify(barber.to_dict()), 201


# Activate a barber
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


# Get all barbers
@app_views.route('/user/barbers/', methods=['GET'])
def get_barbers():
    """Gets user information for all barbers."""
    barbers = []
    for barber in Barber.query.all():
        barbers.append(barber.to_dict())

    return jsonify(barbers)


# Get barbers in a specific location
@app_views.route('/user/barbers/<string:location>', methods=['GET'])
def get_barbers_by_location(location):
    """ Returns all barbers that exactly or closely match the location
    data passed in json.

    :return:
    """
    pass


# Get a barber
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


# Get a barbers reviews
@app_views.route('/user/barber/<barber_id>/reviews', methods=['GET'])
def get_barber_reviews(barber_id):
    """Gets all reviews a barber has."""
    pass


# Update a barber
@login_required
@app_views.route('/user/barber/<barber_id>', methods=['PUT'])
def update_barber(barber_id):
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


@app_views.route('user/barber/<barber_id>/add_style/style_id', methods=['PUT'])
def select_styles(barber_id, style_id):
    """ Adds styles to a barbers list of styles.
    
    Args:
        barber_id (int): Unique id for a barber.
    
    Return: List of barber's styles.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # data = request.get_json()
    # if 'id' not in data:
    #     return make_response(jsonify({'error': 'Missing style id'}), 400)

    barber = Barber.query.filter_by(id=barber_id).first()
    style = Style.query.filter_by(id=style_id).first()
    if barber is None or style is None:
        abort(404)

    barber.styles.append(style)
    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


@app_views.route('user/barber/<barber_id>/remove_style/<style_id>', methods=['PUT'])
def unselect_a_styles(barber_id, style_id):
    """ Removes a style from the list of a barber's styles
    
    Args:
        barber_id (int): Unique id for a barber.
    
    Return: List of barber's styles.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    # data = request.get_json()
    # if 'id' not in data:
    #     return make_response(jsonify({'error': 'Missing style id'}), 400)

    barber = Barber.query.filter_by(id=barber_id).first()
    style = Style.query.filter_by(id=style_id).first()
    if barber is None or style is None:
        abort(404)

    barber.styles.remove(style)
    db.session.add(barber)
    db.session.commit()

    return jsonify(barber.to_dict())


# Deletes a barber
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
