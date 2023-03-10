from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('desire_update', 'invitation_friend', 'paid_subscription', avatar)
        widgets = {
            'desire_update': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'invitation_friend': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'paid_subscription': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'avatar': forms.ClearableFileInput(),
        }


class CustomProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = ('desire_update', 'invitation_friend', 'paid_subscription',)


class CustomProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ('desire_update', 'invitation_friend', 'paid_subscription',)
