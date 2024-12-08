from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from quiz.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, ConfirmUserAPIView, SubjectsAPIView, \
    TestsAPIView, SubjectDetailAPIView, TestDetailAPIView, QuestionsAPIView, QuestionDetailAPIView, ShopGetItemAPIView, \
    ShopBuyItemAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('confirm-user/', ConfirmUserAPIView.as_view()),
    path('subjects/', SubjectsAPIView.as_view()),
    path('subjects/<int:pk>/', SubjectDetailAPIView.as_view()),
    path('tests/', TestsAPIView.as_view()),
    path('tests/<int:pk>/', TestDetailAPIView.as_view()),
    path('questions/', QuestionsAPIView.as_view()),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view()),
    path('shop/', ShopGetItemAPIView.as_view()),
    path('shop/buy/', ShopBuyItemAPIView.as_view()),
]
