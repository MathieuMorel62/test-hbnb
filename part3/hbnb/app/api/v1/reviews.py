from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Model de request pour une review
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model de response pour une review
review_response = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})

# Route pour la liste des reviews
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    def post(self):
        """Register a new review"""
        try:
            current_user = get_jwt_identity()
            review_data = api.payload.copy()

            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'message': 'Place not found'}, 404

            if place.owner.id == current_user:
                return {'error': 'You cannot review your own place'}, 400
            
            existing_reviews = facade.get_reviews_by_place(review_data.get('place_id'))
            for review in existing_reviews:
                if review.user.id == current_user:
                    return {'error': 'You have already reviewed this place'}, 400

            review_data['user_id'] = current_user
            review = facade.create_review(review_data)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }, 201
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response)
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        } for review in reviews]

# Route pour une review spécifique
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")
            if review.user.id != current_user:
                return {'error': 'Unauthorized action'}, 403

            review = facade.update_review(review_id, api.payload)
            return {
                'message': 'Review updated successfully',
                'review': {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id,
                    'place_id': review.place.id
                }
            }
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}
        api.abort(404, "Review not found")

# Route pour la liste des reviews d'un lieu
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_response)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            } for review in reviews]
        except ValueError as e:
            api.abort(404, str(e))
