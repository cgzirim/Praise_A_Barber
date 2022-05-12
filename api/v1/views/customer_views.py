# from .v1 import app_views
# from api.v1 import app_views
from api.v1.views import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style

@app_views.route('/')
def index():
    """
        Test view point to ensure that the endpoint is connecting
    :return:
    """
    return 'Hello Africa!'


@app_views.route('/user/cust/', methods=['POST'])
def create_a_cust():
    pass


@app_views.route('/user/cust/', methods=['GET'])
def get_custs():
    pass


@app_views.route('/user/cust/<id>', methods=['GET'])
def get_a_cust(id):
    pass


@app_views.route('/user/cust/<id>', methods=['PUT'])
def edit_a_cust(id):
    pass


@app_views.route('/user/cust/', methods=['DEL'])
def delete_a_use():
    pass
