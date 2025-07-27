# app/api/v1/__init__.py

from flask import Blueprint
from flask_restx import Api

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
api = Api(app_views, version="1.0", title="HBnB API", description="Places API")

# ✅ Import and register namespaces here
from app.api.v1.places import places_ns
api.add_namespace(places_ns, path="/places")
