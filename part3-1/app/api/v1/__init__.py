from flask import Flask
from flask_cors import CORS
from app.persistence.repository import db

def create_app():
    app = Flask(__name__)


    CORS(app,
         origins="http://127.0.0.1:5500",
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.api.v1 import app_views
    app.register_blueprint(app_views, url_prefix="/api/v1")

    
    @app.after_request
    def apply_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    return app
