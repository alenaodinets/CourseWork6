from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms

from main.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ChangeUserPasswordForm(StyleFormMixin, PasswordResetForm):
    pass


class UserModerationForm(UserProfileForm):
    class Meta:
        model = User
        fields = ('is_active',)
