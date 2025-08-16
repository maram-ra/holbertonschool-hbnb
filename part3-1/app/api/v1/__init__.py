from flask import Flask
from flask_cors import CORS
from app.persistence.repository import db

def create_app():
    app = Flask(__name__)


    CORS(
        app,
        resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}},
        supports_credentials=True
    )

    # DB config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprint with prefix
    from app.api.v1 import app_views
    app.register_blueprint(app_views, url_prefix="/api/v1")

    return app
