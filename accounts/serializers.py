from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Profile, AccessTimes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", 'email', 'password', 'username', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True, "required": False}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'photo', 'address', 'city', 'gender', 'phone', 'user', 'birth_date']
        extra_kwargs = {
            'user': {'required': False}
        }


class AccessTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTimes
        fields = ['start_hour', 'finish_hour']
