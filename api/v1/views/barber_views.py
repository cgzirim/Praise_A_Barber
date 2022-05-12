from api.v1.views import app_views
from models.user import User
from models.ops import Comments
from models.barber import Barber, BarberRating, Style


@app_views.route('/user/barber/', methods=['POST'])
def create_barber():
    pass


@app_views.route('/user/barber/activate/<id>', methods=['PUT'])
def create_barber():
    """
        This function activates a barber's account
    :return:
    """
    pass


@app_views.route('/user/barber/', methods=['GET'])
def get_barbers():
    """
        This function gets all barbers enrolled
    :return:
    """
    pass


@app_views.route('/user/barber/<id>', methods=['GET'])
def get_a_barber(id):
    """
        This function get a particular user by it's id
    :param id: unique id of a barber
    :return:
    """
    pass


@app_views.route('/user/barber/<id>', methods=['PUT'])
def edit_barber(id):
    pass


@app_views.route('/user/barber/', methods=['DEL'])
def delete_a_barber():
    pass


@app_views.route('/barbers', methods=['GET'])
def get_barbers_by_location():
    """
    the function will return all barbers that exactly or closely match the location
    data passed in json
    :return:
    """
    pass


@app_views.route('/barber/select-style', methods=['POST'])
def select_styles():
    """
        The function will enable a barber to select the styles from a list of styles
        by their id in a list. This styles will be saved in the database for this barber.
    :return:
    """
    pass


@app_views.route('/barber/unselect-style', methods=['POST'])
def unselect_a_styles():
    """
        The function will enable a barber to unselect the styles from a list of styles
        by their ids. This styles will be removed from the database for this barber.
    :return:
    """
    pass
