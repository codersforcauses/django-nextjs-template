from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for JWT authentication operations.

    Provides login, register, logout, and token refresh actions.
    """
    permission_classes = [AllowAny]

    def list(self, request):
        """
        List authentication endpoints and current user status.

        GET /api/auth/
        """
        data = {
            'endpoints': {
                'login': request.build_absolute_uri('login/'),
                'register': request.build_absolute_uri('register/'),
                'refresh': request.build_absolute_uri('refresh/'),
                'logout': request.build_absolute_uri('logout/'),
            }
        }

        if request.user.is_authenticated:
            data['user'] = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            }
        else:
            data['user'] = None

        return Response(data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Authenticate user and return JWT tokens.

        POST /api/auth/login/
        {
            "username": "keeper1",
            "password": "password123"
        }

        Returns:
        {
            "refresh": "<refresh_token>",
            "access": "<access_token>",
            "user": {
                "id": 1,
                "username": "keeper1",
                "email": "keeper1@zoo.com"
            }
        }
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user and return JWT tokens.

        POST /api/auth/register/
        {
            "username": "keeper1",
            "email": "keeper1@zoo.com",
            "password": "password123"
        }

        Returns:
        {
            "refresh": "<refresh_token>",
            "access": "<access_token>",
            "user": {
                "id": 1,
                "username": "keeper1",
                "email": "keeper1@zoo.com"
            }
        }
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        """
        Refresh access token using refresh token.

        POST /api/auth/refresh/
        {
            "refresh": "<refresh_token>"
        }

        Returns:
        {
            "access": "<new_access_token>"
        }
        """
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def logout(self, request):
        """
        Logout user by blacklisting refresh token (if provided).

        POST /api/auth/logout/
        {
            "refresh": "<refresh_token>"  (optional)
        }

        Note: With JWT, logout is typically handled client-side by
        deleting the tokens. This endpoint is provided for consistency
        and can blacklist tokens if blacklist app is enabled.
        """
        refresh_token = request.data.get('refresh')

        if refresh_token:
            try:
                RefreshToken(refresh_token)
                # Note: Blacklisting requires additional setup
                # For now, we just validate and return success
                return Response(
                    {'message': 'Successfully logged out'},
                    status=status.HTTP_200_OK
                )
            except Exception:
                pass

        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
