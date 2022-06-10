from api.v1 import db, app
from api.v1.views import app_views
from models.user import User
from models.ops import Review
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
        print(request.headers)
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


@app_views.route('/user/barber/login', methods=['POST'])
def loginWithJson():
    """
        This is the login function, data will be collected with json
    :return: jwt token
    """
    # creates dictionary of form data
    auth = request.get_json()
    print(auth)

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

        return make_response(jsonify({
            'status': 'ok',
            'message': 'login successful',
            'token': token
            }), 201)
    # returns 403 if password is wrong
    return make_response(jsonify({'message': 'password incorrect'}), 403)


@app_views.route('/user/barber/form/login', methods=['POST'])
def loginWithFormdata():
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


@app_views.route('/user/logout')
def logout():
    """ function to handle user logout by expiring session token"""
    pass


@app_views.route('/dashboard')
@login_required
def dashboard(current_user):
    """Dashboard view"""
    print(current_user)
    # barber = Barber.query.filter(Barber.username.ilike(username)).first()
    # # print(barber.to_dict())
    # if barber is None:
    #     abort(404)

    return jsonify({
        'status': 'ok',
        'user': current_user.to_dict()
        }), 200


# Create a barber
@app_views.route("/user/barber/", methods=["POST"])
def create_barber():
    """Creates a new barber.

    Return: A dictionary representation of the instance of the new barber.
    """
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    compulsory_data = [
        "username",
        "password",
        # "email",
        # "phone",
        # "country",
        # "state",
        # "city",
        # "address",
        # ^ Commented out for development's sake
    ]
    for attr in compulsory_data:
        if attr not in data:
            return make_response(jsonify({"error": "Missing " + attr}), 400)

    # Throw an error when a request contains a unique attr that already exits
    # in the table.
    if "id" in data:
        if Barber.query.filter_by(id=data["id"]).first():
            return make_response(jsonify({"error": "id exists"}), 400)
    if Barber.query.filter_by(username=data["username"]).first():
        return make_response(jsonify({"error": "Username exists"}), 400)
    if Barber.query.filter_by(email=data["email"]).first():
        return make_response(jsonify({"error": "Email exists"}), 400)
    if Barber.query.filter_by(phone=data["phone"]).first():
        return make_response(jsonify({"error": "Phone number exists"}), 400)

    # If data.styles is true, create the styles
    if "styles" in data:
        if data["styles"]:
            styles = []
            for style in data["styles"].split(","):
                style_obj = Style.query.filter_by(name=style.strip()).first()
                if style_obj is None:
                    return make_response(
                        jsonify({"error": "Style, {}, does't exist".format(style)})
                    )
                else:
                    styles.append(style_obj)
            data["styles"] = styles

    data['id'] = str(uuid.uuid4())
    data['password'] = generate_password_hash(data['password'])

    try:
        barber = Barber(**data)
        db.session.add(barber)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return "{}: {}".format(e.__class__.__name__, repr(e.orig)), 400

    return make_response(jsonify(barber.to_dict()), 201)


# Activate a barber
@app_views.route("/user/barber/activate/<barber_id>", methods=["PUT"])
def activate_barber(barber_id):
    """
        This function activates a barber's account
    :return:
    """
    barber = Barber.query.filter_by(id=barber_id).first()
    if barber is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for k, v in request.get_json().items():
        setattr(barber, k, v)

    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


# Get all barbers
@app_views.route("/user/barbers/", methods=["GET"])
def get_barbers():
    """Gets user information for all barbers."""
    state = request.args.get("state")
    city = request.args.get("city")
    barbers = []

    if state or city:
        # Get all barbers in the city of a state
        if state and city:
            for b in Barber.query.filter(
                Barber.state.ilike(state), Barber.city.ilike(city)
            ).all():
                barbers.append(b.to_dict())
        # Get all barbers in a state
        elif state:
            for b in Barber.query.filter(Barber.state.ilike(state)).all():
                barbers.append(b.to_dict())
        # Get all barbers in a city
        elif city:
            print(city)
            for b in Barber.query.filter(Barber.city.ilike(city)).all():
                barbers.append(b.to_dict())
    else:
        # Get all barbers irrespective of their state or city
        for barber in Barber.query.all():
            barbers.append(barber.to_dict())

    return jsonify(barbers)


# Get barbers in a specific state, city
@app_views.route("/user/barbers/<string:state>", methods=["GET"])
@app_views.route("/user/barbers/<string:state>/<string:city>", methods=["GET"])
def get_barbers_by_location(state, city=None):
    """Returns all barbers that exactly or closely match the location
    data passed in json.
    """
    barbers = []

    # Get barbers in a city if city is passed otherwise gets barbers in a state
    if city:
        for b in Barber.query.filter(
            Barber.state.ilike(state), Barber.city.ilike(city)
        ).all():
            barbers.append(b.to_dict())
    else:
        for b in Barber.query.filter(Barber.state.ilike(state)).all():
            barbers.append(b.to_dict())

    return jsonify(barbers)


# Get a barber
@app_views.route("/user/barber/<username>", methods=["GET"])
def get_a_barber(username):
    """Gets a particular barber by it's id
    Args:
        username (str): Unique username of a barber.

    Returns information of a barber.
    """
    # filter = request.args.get("filter")

    barber = Barber.query.filter(Barber.username.ilike(username)).first()
    # print(barber.to_dict())
    if barber is None:
        abort(404)

    # if filter == "data":
    #     return jsonify(barber.to_dict())
    # if filter == "posts":
    #     return jsonify("comming soon")
    # if filter == "reviews":
    #     reviews = [review.to_dict() for review in barber.reviews]
    #     print(reviews)
    #     return jsonify(reviews)

    return jsonify(barber.to_dict()), 200


# Update a barber
@login_required
@app_views.route('/user/barber/<username>', methods=['PUT'])
def update_barber(username):
    """Updates a barber.
    Args:
        barber_id (int): Unique username of a barber.
    """
    barber = Barber.query.filter(Barber.username.ilike(username)).first()
    if barber is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for k, v in request.get_json().items():
        if k == 'styles':
            continue
        setattr(barber, k, v)
    setattr(barber, "updated_date", datetime.utcnow())

    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


# requires login
@app_views.route("user/barber/<string:barber_usernm>/add_style/<string:style_nm>", methods=["PUT"])
def select_styles(barber_usernm, style_nm):
    """Adds styles to a barbers list of styles.

    Args:
        barber_id (int): Unique id for a barber.

    Return: List of barber's styles.
    """
    barber = Barber.query.filter(Barber.username.ilike(barber_usernm)).first()
    if barber is None:
        return make_response(jsonify({"error": barber_usernm + " does not exist"}), 401)

    style = Style.query.filter(Style.name.ilike(style_nm)).first()
    if style is None:
        return make_response(jsonify({"error": "Hairstyle does not exist"}), 401)

    barber.styles.append(style)
    db.session.add(barber)
    db.session.commit()
    return jsonify(barber.to_dict())


# requires login
@app_views.route("user/barber/<string:barber_usernm>/remove_style/<string:style_nm>", methods=["PUT"])
def unselect_a_styles(barber_usernm, style_nm):
    """Removes a style from the list of a barber's hairstyles

    Args:
        barber_id (int): Unique id for a barber.

    Return: List of barber's hairstyles.
    """

    barber = Barber.query.filter(Barber.username.ilike(barber_usernm)).first()
    if barber is None:
        return make_response(jsonify({"error": barber_usernm + " does not exist"}), 401)

    style = Style.query.filter(Style.name.ilike(style_nm)).first()
    if style is None:
        return make_response(jsonify({"error": "Hairstyle does not exist"}), 401)

    barber.styles.remove(style)
    db.session.add(barber)
    db.session.commit()

    return jsonify(barber.to_dict())


# Deletes a barber
@app_views.route("/user/barber/<string:barber_usernm>", methods=["DELETE"])
def delete_a_barber(barber_usernm):
    """Deletes a barber.
    Args:
        barber_id (int): Unique id of a barber.
    """
    barber = Barber.query.filter(Barber.username.ilike(barber_usernm)).first()
    if barber is None:
        abort(404)

    db.session.delete(barber)
    db.session.commit()
    del barber
    return jsonify({})
