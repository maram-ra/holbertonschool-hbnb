#!/usr/bin/python3
"""Initialize the API views package"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views so they get registered
from app.api.v1.amenities import *
