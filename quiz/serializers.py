from rest_framework import serializers
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