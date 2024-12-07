from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import User, Test


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])
        user.save()
        user.create_verification_code
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ConfSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            attrs["access"] = str(token.access_token)
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token.")
        return attrs

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('name', 'subject', 'level', 'balls')