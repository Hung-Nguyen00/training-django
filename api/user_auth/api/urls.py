from django.urls import path, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView

from user_auth.api.views import (
    CustomConfirmEmailView,
    CustomLoginView,
    CustomRegisterView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    path("auth/registration/verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("auth/password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("auth/password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="rest_password_reset_confirm"),
    path("token/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("account/activate/<key>/", CustomConfirmEmailView.as_view(), name="verify-email"),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
        name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
        name='account_confirm_email'),
]
