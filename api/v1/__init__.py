import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask import jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

# from api.v1.views import app_views

# Instantiate flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0:*"}})

# Set configs
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swagger configs
SWAGGER_URL = '/api/v1/docs'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Praise A Barber Api"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

# Instantiate db object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.v1.views import app_views

app.register_blueprint(app_views)
