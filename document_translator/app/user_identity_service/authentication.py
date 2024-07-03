import jwt
from .models import User
from jwt.exceptions import InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
 
class UserAuthentication(BaseAuthentication):
 
    @staticmethod
    def decode_msal_token(token: str, secret: str = None, algorithms: list = ['RS256']):
        try:
            if secret:
                payload = jwt.decode(token, secret, algorithms=algorithms)
            else:
                payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
 
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
 
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')
            data = self.decode_msal_token(token)
            if data is None:
                raise AuthenticationFailed('Invalid token')
 
            user_email = data.get('unique_name')
            if not user_email:
                raise AuthenticationFailed('Token does not contain user ID')
 
            user = User.objects.get(email=user_email)
            return (user, token)
        except Exception as e:
            raise AuthenticationFailed(f"Authentication failed: {str(e)}")