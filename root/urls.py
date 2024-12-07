from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from quiz.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, UserConfirmationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('confirm-user/', UserConfirmationView.as_view()),
]
