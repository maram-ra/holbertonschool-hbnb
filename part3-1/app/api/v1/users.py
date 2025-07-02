from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request

users_api = Namespace('users', description='User operations')
admin_ns = Namespace('admin', description='Admin-only ops')

def is_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)

# Models
admin_user_update_model = admin_ns.model('AdminUserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'email': fields.String(required=False),
    'password': fields.String(required=False)
})

user_model = users_api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

user_update_model = users_api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

# Admin routes
@admin_api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @admin_api.expect(admin_user_update_model)
    def put(self, user_id):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = admin_api.payload
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user['id'] != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

# User routes
@users_api.route('/')
class UserList(Resource):
    @jwt_required()
    @users_api.expect(user_model, validate=True)
    def post(self):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = users_api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user['id'],
            'first_name': new_user['first_name'],
            'last_name': new_user['last_name'],
            'email': new_user['email']
        }, 201

    @users_api.response(200, 'List of users retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return users, 200

@users_api.route('/<user_id>')
class UserResource(Resource):
    @users_api.response(200, 'User details retrieved successfully')
    @users_api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }, 200

    @jwt_required()
    @users_api.expect(user_update_model)
    def put(self, user_id):
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized'}, 403

        data = users_api.payload

        if 'email' in data or 'password' in data:
            return {'error': 'Cannot modify email or password through this endpoint'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
