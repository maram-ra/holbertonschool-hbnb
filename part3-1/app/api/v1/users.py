from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services import facade

# User namespace
users_api = Namespace('users', description='User operations')

# Admin-only namespace
admin_ns = Namespace('admin', description='Admin operations')

def is_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)

# Models
user_model = users_api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

user_update_model = users_api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    # Email and password cannot be changed via this endpoint
})

admin_user_update_model = admin_ns.model('AdminUserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'email': fields.String(required=False),
    'password': fields.String(required=False)
})

# Routes for regular users

@users_api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @users_api.response(200, 'User details retrieved successfully')
    @users_api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
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
        """Update user details (only self; cannot change email or password here)"""
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized'}, 403

        data = request.json or {}

        if 'email' in data or 'password' in data:
            return {'error': 'Cannot modify email or password through this endpoint'}, 400

        try:
            facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


# Admin-only routes

@admin_ns.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @admin_ns.expect(user_model)
    def post(self):
        """Create a new user (Admins only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json or {}
        if facade.get_user_by_email(data.get('email')):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(data)
        return {
            'id': new_user['id'],
            'first_name': new_user['first_name'],
            'last_name': new_user['last_name'],
            'email': new_user['email']
        }, 201

@admin_ns.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @admin_ns.expect(admin_user_update_model)
    def put(self, user_id):
        """Modify any user (Admins only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json or {}
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user['id'] != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@admin_ns.route('/users')
class AdminUserList(Resource):
    @jwt_required()
    def get(self):
        """Get all users (Admins only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403
        users = facade.get_all_users()
        return users, 200
