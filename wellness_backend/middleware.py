from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """Middleware для проверки JWT токенов на защищенных маршрутах"""
    
    PROTECTED_PATHS = [
        '/api/profiles/',
        '/api/food-diary/',
        '/api/exercises/',
        '/api/progress/',
    ]
    
    def process_request(self, request):
        # Пропускаем аутентификацию и админку
        if request.path.startswith('/api/auth/') or request.path.startswith('/admin/'):
            return None
            
        # Проверяем защищенные маршруты
        if any(request.path.startswith(path) for path in self.PROTECTED_PATHS):
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(
                    jwt_auth.get_raw_token(jwt_auth.get_header(request))
                )
                user = jwt_auth.get_user(validated_token)
                request.user = user
            except (InvalidToken, TokenError, TypeError):
                return JsonResponse({'error': 'Недействительный токен'}, status=401)
        
        return None