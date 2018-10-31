from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import LHUser

class DefaultRegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    class Meta:
        model = LHUser
        fields = ['email', 'password', 'password_confirm']

    def validate_password(self, password):
        user = LHUser(self.initial_data)
        validate_password(password, user=user)
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise ValidationError('Passwords don\'t match')
        return attrs

    def create(self, validated_data):
        data = validated_data.copy()
        del data['password_confirm']
        return self.Meta.model.objects.create_user(**data)
