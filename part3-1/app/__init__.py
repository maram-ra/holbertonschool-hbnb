from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.persistence.repository import db

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')

    # Import namespaces here (avoid circular imports)
    from app.api.v1.users import users_api, admin_ns
    from app.api.v1.amenities import amenities_ns
    from app.api.v1.places import places_ns

    # Register namespaces with distinct paths
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
