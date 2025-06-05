from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
