from rest_framework import serializers

# из списка выкинуты User,
from backend.models import User


#class ContactSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Contact
    #     fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
    #     read_only_fields = ('id',)
    #     extra_kwargs = {
    #         'user': {'write_only': True}
    #     }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name',  'email',)
        read_only_fields = ('id',)

