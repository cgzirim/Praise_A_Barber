# from .v1 import app_views
# from api.v1 import app_views
from app.v1.views import app_views


@app_views.route('/')
def index():
    return 'Hello Africa!'
