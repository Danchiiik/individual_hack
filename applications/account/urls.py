from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from applications.account.views import ChangePasswordApiView, ForgotPasswordFinishApiview, ForgotRasswordApiView, UserRegisterApiView, ActivationApiView


urlpatterns = [
    path('register/', UserRegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('change_password/', ChangePasswordApiView.as_view()),
    path('forgot_password/', ForgotRasswordApiView.as_view()),
    path('forgot_password_finish/', ForgotPasswordFinishApiview.as_view()),
]
