from app.v1.views import app_views
from app.v1.models.ops import Comments
from app.v1.models.user import User
from app.v1.models.barber import Barber, BarberRating, Style


@app_views.route('/barber/rate', methods=['POST'])
def rate_a_barber():
    pass


@app_views.route('/barber/rate', methods=['POST'])
def rate_a_barber():
    pass


@app_views.route('/style/add', methods=['POST'])
def add_styles():
    """
        This function will enable an admin add styles into the database
    :return:
    """
    pass


@app_views.route('/style/add', methods=['POST'])
def remove_styles():
    """
        This function will enable an admin remove styles from the database
    :return:
    """
    pass
