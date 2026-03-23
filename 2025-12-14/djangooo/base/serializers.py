from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    # Defining password as write_only so it won't be returned in any Response
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Using create_user to handle password hashing automatically
        return User.objects.create_user(**validated_data)