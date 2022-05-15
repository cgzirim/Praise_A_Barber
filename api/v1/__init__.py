import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask import jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

# from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0:*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.v1.views import app_views

app.register_blueprint(app_views)
