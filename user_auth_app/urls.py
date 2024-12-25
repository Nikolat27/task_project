from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user_app"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"), # Login the user using JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Refresh token for JWT
]
