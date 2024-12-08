import datetime
from django.utils.timezone import now
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status, permissions, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.filters import TestFilter, SubjectFilter, QuestionsFilter
from quiz.models import User, Subjects, Test, Question, Shop
from quiz.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, ConfSerializer, \
    SubjectsSerializer, TestsSerializer, QuestionsSerializer, ShopSerializer, BuyItemInShopSerializer, \
    ProfileUserSerializer, ChangePasswordSerializer


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
        print(request.user)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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


class ConfirmUserAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @extend_schema(request=ConfSerializer, tags=['auth'])
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ConfSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data.get('code'))
            self.verify_code(user, serializer.validated_data.get("code"))
            data = {
                'status': 'Success',
                'message': f'Confirmation code {serializer.validated_data["code"]}',
                # 'access_token': user.token()['access_token'],
                # 'refresh_token': user.token()['refresh_token']
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
            expire_time__gte=now()
        )
        if not verification.exists():
            raise ValidationError({
                'status': 'Fail',
                'message': 'Code is invalid or expired.'
            })
        verification.update(is_confirmed=True)
        user.is_verified = True
        user.save()
        return user

# Test Endpoints

@extend_schema(
        request=SubjectsSerializer,
    )
class SubjectsAPIView(generics.ListAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = SubjectFilter


    # def get(self, request):
    #     subjects = Subjects.objects.all()
    #     serializer = SubjectsSerializer(subjects, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class SubjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer

class TestsAPIView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['subject', ]
    # search_fields = ['subject__name', ]
    filterset_class = TestFilter

class TestDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Test.objects.all()
    serializer_class = TestsSerializer

class QuestionsAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = QuestionsFilter

class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ShopGetItemsAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    @extend_schema(
        request=ShopSerializer,
    )
    def get(self, request):
        shop = Shop.objects.all()
        serializer = ShopSerializer(shop, many=True)
        return Response(serializer.data)

class ShopRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ShopBuyItemAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    @extend_schema(request=BuyItemInShopSerializer)
    def post(self, request):
        user = request.user
        serializer = BuyItemInShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_item = Shop.objects.filter(name=serializer.validated_data.get('name')).first()

        if not shop_item:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.balls < shop_item.price:
            return Response({"error": "Not enough balls to buy the item."}, status=status.HTTP_400_BAD_REQUEST)

        user.balls -= shop_item.price
        user.save()
        user.gifts.add(shop_item)

        return Response({"message": "Item purchased successfully!"}, status=status.HTTP_200_OK)

class ProfileUserGetUpdateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        user = request.user
        serializer = ProfileUserSerializer(user)
        return Response(serializer.data)
    @extend_schema(request=ProfileUserSerializer)
    def put(self, request):
        user = request.user
        serializer = ProfileUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ChangePasswordAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    @extend_schema(request=ChangePasswordSerializer, tags=['auth'])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# test user
# username: John, password: 1111
# refresh_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzc2NDM5OSwiaWF0IjoxNzMzNjc3OTk5LCJqdGkiOiJhOTQzYjA4NzMzZWE0MGIyODUxNGM5ZGM4MTk2YWIzZiIsInVzZXJfaWQiOjJ9.juUd41UmH26INY8O25ujqpeA6yyF_3e5coIKt-cf4mA