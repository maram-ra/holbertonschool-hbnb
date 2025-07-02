from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        user = get_jwt_identity()
        data = api.payload
        data['user_id'] = user['id']

        # Get place to prevent reviewing your own
        place = facade.get_place_by_id(data['place_id'])
        if not place:
            api.abort(404, "Place not found")

        if place['owner_id'] == user['id']:
            api.abort(400, "You cannot review your own place")

        # Check if already reviewed
        existing = facade.get_user_review_for_place(user['id'], data['place_id'])
        if existing:
            api.abort(400, "You have already reviewed this place")

        try:
            review = facade.create_review(data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        r = facade.get_review(review_id)
        if not r:
            api.abort(404, "Review not found")
        return r.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != user['id']:
            api.abort(403, "You are not authorized to update this review")

        try:
            updated = facade.update_review(review_id, api.payload)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, review_id):
        user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != user['id']:
            api.abort(403, "You are not authorized to delete this review")

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, "Place not found")
        return [r.to_dict() for r in reviews], 200
