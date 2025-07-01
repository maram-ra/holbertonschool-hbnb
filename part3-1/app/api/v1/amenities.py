from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

AMENITIES = []

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    def post(self):
        new_amenity = api.payload
        new_amenity['id'] = str(len(AMENITIES) + 1)
        AMENITIES.append(new_amenity)
        return new_amenity, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        return AMENITIES, 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        for amenity in AMENITIES:
            if amenity['id'] == amenity_id:
                return amenity
        api.abort(404, f"Amenity {amenity_id} not found")

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        for amenity in AMENITIES:
            if amenity['id'] == amenity_id:
                data = api.payload
                if not data or 'name' not in data:
                    api.abort(400, "Invalid input data")
                amenity['name'] = data['name']
                return {"message": "Amenity updated successfully"}
        api.abort(404, f"Amenity {amenity_id} not found")
