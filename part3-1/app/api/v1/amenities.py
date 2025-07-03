from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

def is_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    def get(self):
        """List all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        if not data or 'name' not in data:
            return {'error': 'Amenity name is required'}, 400

        try:
            new_amenity = facade.create_amenity(data)
            return new_amenity, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @jwt_required()
    def put(self, amenity_id):
        """Update amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        if not data or 'name' not in data:
            return {'error': 'Amenity name is required'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity, 200
        except Exception as e:
            return {'error': str(e)}, 400

# Export namespace with expected name
amenities_ns = api
