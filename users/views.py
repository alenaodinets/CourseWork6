import secrets
import string
import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, ChangeUserPasswordForm, UserModerationForm
from users.models import User


# Create your views here.

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.verification_code = "".join([str(random.randint(1, 9)) for i in range(10)])
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/register/confirm/{user.verification_code}"
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке{url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def get_object(self, queryset=None):
        return self.request.user


def verification_view(request, token):
    user = User.objects.filter(verification_code=token).first()
    if user:
        user.is_active = True
        user.save()
    return redirect('users:login')


def recover_password(request):
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(10))
    request.user.set_password(password)
    request.user.save()
    message = f"Ваш новый пароль:\n{password}"
    send_mail(
        "Сменить пароль",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    return redirect(reverse('users:user_list'))


class ResetUserPasswordView(PasswordResetView):
    form_class = ChangeUserPasswordForm
    success_url = reverse_lazy('users:login')


    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            try:
                user = User.objects.get(email=email)
                alphabet = string.ascii_letters + string.digits
                password = "".join(secrets.choice(alphabet) for i in range(10))
                user.set_password(password)
                user.save()
                message = f"Ваш новый пароль:\n{password}"
                send_mail(
                    "Сменить пароль",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                return render(self.request, 'password_reset_form.html',
                              {'error_message': 'Пользователь с таким email не найден'})
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    permission_required = ('users.view_user', )


class UserModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserModerationForm
    template_name = 'user_form.html'
    permission_required = ('users.set_active',)

    def get_success_url(self):
        return reverse_lazy('users:users')
