"""Users app serializers."""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        """Meta class."""
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'birth_date', 'password', 'groups')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, data):
        """Define the password."""
        data['password'] = make_password(data['password'])
        return super().create(data)
