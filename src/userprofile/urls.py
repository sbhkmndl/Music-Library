from django.conf.urls import url
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import (UserLoginView,
                    UserCreateView,
                    UserLogoutView,
                    UserForgetPasswordView,
                    ResetPasswordView,
                    ChangePasswordView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('forgetPassword/', UserForgetPasswordView.as_view(), name='password_forget'),
    re_path(r'^resetPassword/(?P<key>[a-zA-z0-9]+)/$', ResetPasswordView.as_view(), name='password_reset'),
    path('changePassword/', ChangePasswordView.as_view(), name='password_change'),
]
