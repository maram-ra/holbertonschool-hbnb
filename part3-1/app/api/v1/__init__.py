from flask import Flask
from flask_cors import CORS
from app.persistence.repository import db  # تأكد أن db موجود في هذا المسار

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.api.v1 import app_views
    app.register_blueprint(app_views)

    return app
