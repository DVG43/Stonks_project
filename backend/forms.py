from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name',)


class CustomProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = ('desire_update', 'invitation_friend', 'paid_subscription',)


class CustomProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ('desire_update', 'invitation_friend', 'paid_subscription',)
