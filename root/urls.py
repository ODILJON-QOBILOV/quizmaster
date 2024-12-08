from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from quiz.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, ConfirmUserAPIView, SubjectsAPIView, \
    TestsAPIView, SubjectDetailAPIView, TestDetailAPIView, QuestionsAPIView, QuestionDetailAPIView, ShopGetItemsAPIView, \
    ShopBuyItemAPIView, ProfileUserGetUpdateAPIView, ShopRetrieveAPIView, ChangePasswordAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # auth
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('confirm-user/', ConfirmUserAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    # subjects
    path('subjects/', SubjectsAPIView.as_view()),
    path('subjects/<int:pk>/', SubjectDetailAPIView.as_view()),
    # tests
    path('tests/', TestsAPIView.as_view()),
    path('tests/<int:pk>/', TestDetailAPIView.as_view()),
    # questions
    path('questions/', QuestionsAPIView.as_view()),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view()),
    # shop
    path('shop/', ShopGetItemsAPIView.as_view()),
    path('shop/item/<int:pk>/', ShopRetrieveAPIView.as_view()),
    path('shop/buy/', ShopBuyItemAPIView.as_view()),
    # profile
    path('profile/', ProfileUserGetUpdateAPIView.as_view()),
]
