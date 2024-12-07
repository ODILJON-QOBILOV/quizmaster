import datetime

from django.contrib.auth import authenticate
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import User
from quiz.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, ConfSerializer


class RegisterAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RegisterSerializer,
        examples=[
            OpenApiExample(
                name="Example of Request",
                value={
                    'username': 'John',
                    'email': 'example@gmail.com',
                    'password': '1234'
                },
                description="Example of a user registration request"
            )
        ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.create_verification_code
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                name="Example of Login Request",
                value={
                    'username': 'John',
                    'password': '1234'
                },
                description="Example of a user login request"
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({"error": "User account is inactive."}, status=status.HTTP_401_UNAUTHORIZED)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RefreshTokenSerializer,
        examples=[
            OpenApiExample(
                name="Example of Refresh Access Token Request",
                value={
                    'refresh': "asdfgtres2dcvb66njytrdfbhjyw5uythgfd"
                },
                description="Example of a user get another access token request"
            )
        ]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Test Endpoints

class UserConfirmationView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @extend_schema(request=ConfSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ConfSerializer(data=request.data)
        if serializer.is_valid():
            self.verify_code(user, serializer.validated_data.get("code"))
            data = {
                'status': 'Success',
                'message': f'Confirmation code {serializer.validated_data["code"]}',
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token']
            }
        else:
            data = {
                'status': 'Fail',
                'message': serializer.errors
            }
        return Response(data)

    @staticmethod
    def verify_code(user, code):
        verification = user.code.filter(
            code=code,
            is_confirmed=False,
            expire_time__gte=datetime.now()
        )
        if not verification.exists():
            raise ValidationError({
                'status': 'Fail',
                'message': 'Code is invalid or expired.'
            })
        verification.update(is_confirmed=True)
        if user.status == User.UserStatus.INACTIVE:
            user.status = User.UserStatus.ACTIVE
        user.save(update_fields=['status'])






