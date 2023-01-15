from rest_framework import serializers

# из списка выкинуты User,
from backend.models import User, Profile




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name',  'email',)
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'desire_update', 'invitation_friend', 'paid_subscription',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'avatar': {'write_only': True}
        }
