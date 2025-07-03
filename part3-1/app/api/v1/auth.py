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
            # 1) Fetch the User object (not serialized)
            user = facade.get_user_by_email(credentials['email'])
            if not user:
                return {'error': 'Invalid credentials'}, 401

            # 2) Verify password
            if not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            # 3) Generate JWT using object attributes, not subscription
            access_token = create_access_token(
                identity={"id": str(user.id), "is_admin": user.is_admin}
            )
            return {'access_token': access_token}, 200

        except Exception as e:
            # Dump full traceback to console for debugging
            import traceback; traceback.print_exc()
            return {
                'message': 'Internal Server Error',
                'error': str(e)
            }, 500

# Export namespaces
auth_users_ns = users_api
auth_admin_ns = admin_ns
