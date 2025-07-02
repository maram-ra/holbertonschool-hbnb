from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.persistence.repository import user_repo

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Step 1: Get the user data (dict) from facade
        user_data = facade.get_user_by_email(credentials['email'])
        if not user_data:
            return {'error': 'Invalid credentials'}, 401

        # Step 2: Fetch original user object from the repo
        user = user_repo.get(user_data['id'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create access token
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        return {'access_token': access_token}, 200
