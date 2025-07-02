from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

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
        try:
            # Debug: log payload
            print(f"[DEBUG] Login attempt for email: {credentials.get('email')}")

            # Fetch the User object (not serialized)
            user = facade.get_user_by_email(credentials['email'])
            print(f"[DEBUG] Fetched user: {user}")

            if not user:
                print("[DEBUG] No user found")
                return {'error': 'Invalid credentials'}, 401

            # Verify password
            if not user.verify_password(credentials['password']):
                print("[DEBUG] Password verification failed")
                return {'error': 'Invalid credentials'}, 401

            # Create and return token
            access_token = create_access_token(identity={
                'id': str(user.id),
                'is_admin': user.is_admin
            })
            print(f"[DEBUG] Token generated for user id: {user.id}")
            return {'access_token': access_token}, 200

        except Exception as e:
            # Print full traceback on server console
            import traceback; traceback.print_exc()
            # Return error message in response
            return {
                'message': 'Internal Server Error',
                'error': str(e)
            }, 500
