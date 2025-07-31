from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

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
            user = facade.get_user_by_email(credentials['email'])
            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"is_admin": True}
            )

            return {'access_token': access_token}, 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'message': 'Internal Server Error',
                'error': str(e)
            }, 500
