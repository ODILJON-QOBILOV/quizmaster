from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import User, Test, Subjects, Question, Shop


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

# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Test
#         fields = ('name', 'subject', 'level', 'balls')

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

class TestsSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Test
        fields = ('name', 'subject', 'level', 'balls')

class QuestionsSerializer(serializers.ModelSerializer):
    test = serializers.CharField(source='test.name')
    test_level = serializers.CharField(source='test.level')
    test_balls = serializers.IntegerField(source='test.balls')
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('about', 'test', 'test_level', 'test_balls', 'options')

    def get_options(self, object):
        return [
            {
                "name": option.name,
                "is_true": option.is_true
            }
            for option in object.options.all()
        ]

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class BuyItemInShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', )

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'about', 'price', 'discount', 'image', 'is_active')

class ProfileUserSerializer(serializers.ModelSerializer):
    gifts = ShopItemSerializer(many=True, read_only=True)
    role = serializers.CharField(read_only=True)
    balls = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'date_of_birth', 'image', 'about', 'role',
            'level', 'balls', 'gifts', 'is_verified'
        )

class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password']

    def validate(self, attrs):
        user = self.context['request'].user

        current_password = attrs.get('current_password')
        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")

        new_password = attrs.get('new_password')
        if current_password == new_password:
            raise ValidationError("New password cannot be the same as the current password.")

        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user