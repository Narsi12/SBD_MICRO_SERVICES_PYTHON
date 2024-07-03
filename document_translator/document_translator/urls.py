from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView,TokenVerifyView,TokenBlacklistView)
from .settings import APP_NAME

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(f'{APP_NAME}.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),   
]