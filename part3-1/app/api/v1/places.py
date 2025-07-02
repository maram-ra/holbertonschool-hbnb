from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# ----- MODELS -----

# Related models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(),
    'text': fields.String(),
    'rating': fields.Integer(),
    'user_id': fields.String()
})

# Input model for creating/updating places
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Output model for places including ID, owner_id, and reviews
place_output_model = api.inherit('PlaceOutput', place_input_model, {
    'id': fields.String(),
    'owner_id': fields.String(),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# ----- ROUTES -----

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created', model=place_output_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place (authenticated user only)"""
        data = api.payload
        if not data:
            api.abort(400, "No input data provided")

        user = get_jwt_identity()
        data['owner_id'] = user['id']

        try:
            new_place = facade.create_place(data)
            return new_place, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully', model=[place_output_model])
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', model=place_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        return place

    @jwt_required()
    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (only by owner)"""
        user = get_jwt_identity()
        data = api.payload

        if not data:
            api.abort(400, "No input data provided")

        place = facade.get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")

        if place['owner_id'] != user['id']:
            api.abort(403, "You are not authorized to update this place")

        try:
            updated = facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}
        except Exception as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place (only by owner)"""
        user = get_jwt_identity()
        place = facade.get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")

        if place['owner_id'] != user['id']:
            api.abort(403, "You are not authorized to delete this place")

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200
