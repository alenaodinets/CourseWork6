from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users import apps
from users.views import UserLoginView, RegisterView, verification_view, ProfileView, recover_password, \
    ResetUserPasswordView, UserListView, UserModerationView

app_name = apps.UsersConfig.name


urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/confirm/<str:token>/', verification_view, name='verification'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('recover/', recover_password, name='recover'),
    path('password_reset/',
         ResetUserPasswordView.as_view(template_name="password_reset_form.html",
                                       email_template_name="password_reset_email.html",
                                       success_url=reverse_lazy("users:login")),
         name='password_reset'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
                                          success_url=reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('users/', UserListView.as_view(), name='users'),
    path('user/<int:pk>/', UserModerationView.as_view(), name='user_update')
]
