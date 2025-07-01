from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    def post(self):
        try:
            r = facade.create_review(api.payload)
            return r.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    def get(self):
        result = [r.to_dict() for r in facade.get_all_reviews()]
        return result, 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        r = facade.get_review(review_id)
        if not r:
            api.abort(404, "Review not found")
        return r.to_dict(), 200

    @api.expect(review_model)
    def put(self, review_id):
        try:
            r = facade.update_review(review_id, api.payload)
            if not r:
                api.abort(404, "Review not found")
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))

    def delete(self, review_id):
        if facade.delete_review(review_id):
            return {"message": "Review deleted successfully"}, 200
        api.abort(404, "Review not found")

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, "Place not found")
        return [r.to_dict() for r in reviews], 200
