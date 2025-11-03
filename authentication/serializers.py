import re

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email, RegexValidator
from orjson import orjson
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authentication.models import User, Follow, Notifications, Sessions
from root.settings import redis


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
        read_only_fields = ('id', 'date_joined', 'last_login')

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_.-]+$',
        message="Foydalanuvchi nomida faqat harflar, raqamlar, nuqta, pastki chiziq va chiziqcha bo‘lishi mumkin."
    )

    def validate_username(self, value):
        self.username_validator(value)

        if len(value) < 3:
            raise ValidationError("Foydalanuvchi nomi 3 ta belgidan kam bo‘lmasligi kerak.")

        reserved = ["admin", "root", "system", "null"]
        if value.lower() in reserved:
            raise ValidationError("This username is not allowed.")

        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError("This username is already taken.")

        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError('Elektron pochta manzili yaroqsiz.')

        if User.objects.filter(email=value).exists():
            raise ValidationError('Bu elektron pochta manzili ro‘yxatdan o‘tgan.')

        return value

    def validate_password(self, value):
        if len(value) < 3:
            raise ValidationError('Parol uzunligi kamida 4 ta belgi bo‘lishi lozim.')
        if len(value) > 20:
            raise ValidationError('Parol 20 ta belgidan ortiq bo‘lmasligi kerak.')
        if not re.search(r'\d', value):
            raise ValidationError('Parolda kamida bitta son bo‘lishi lozim.')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Parolda kamida bitta harf bo‘lishi lozim.')

        return make_password(value)


class VerifyCodeSerializer(Serializer):
    code = CharField(max_length=6)

    def validate_code(self, value):
        data = redis.get(value)
        if not data:
            raise ValidationError("Code notog'ri")
        user_data = orjson.loads(data)
        self.context['user_data'] = user_data
        return value


class UserUpdateSerializer(UserModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'username', 'bio', 'city')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(Serializer):
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError('Kiritilgan parollar o‘zaro mos emas.')
        if len(new_password) < 4:
            raise ValidationError('Parol kamida 4 ta belgidan iborat bo‘lishi kerak.')
        if len(new_password) > 20:
            raise ValidationError('Parol 20 ta belgidan oshmasligi kerak.')
        if not re.search(r'\d', new_password):
            raise ValidationError('Parol kamida bitta raqamdan iborat bo‘lishi kerak.')
        if not re.search(r'[A-Za-z]', new_password):
            raise ValidationError('Parol kamida bitta harfdan iborat bo‘lishi kerak.')

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class FollowingModelSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following', 'follower', 'created_at')
        read_only_fields = ('created_at', 'follower')

    def validate_following(self, value):
        user = self.context['request'].user
        if user != value:
            Notifications.objects.create(
                recipient=value,
                sender=user,
                message='started following you',
                type=Notifications.NotificationType.FOLLOWED.value
            )
        if user == value:
            raise ValidationError("Siz ozingizga ozingiz obuna bololmaysiz")
        return value


class NotificationModelSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('id', 'recipient', 'sender', 'message', 'created_at', 'is_read')


class SessionModelSerializer(ModelSerializer):
    class Meta:
        model = Sessions
        fields = ('id', 'device_name', 'ip_address', 'user')
        read_only_fields = ('id',)
