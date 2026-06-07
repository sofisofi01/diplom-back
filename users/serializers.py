from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    height = serializers.FloatField(required=False)
    weight = serializers.FloatField(required=False)
    gender = serializers.ChoiceField(choices=['male', 'female'], required=False)
    age = serializers.IntegerField(required=False, min_value=1, max_value=120)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name',
            'height', 'weight', 'gender', 'age',
        )

    def create(self, validated_data):
        from profiles.models import Profile

        height = validated_data.pop('height', 170)
        weight = validated_data.pop('weight', 70)
        gender = validated_data.pop('gender', 'male')
        age = validated_data.pop('age', None)

        # создаем пользователя (create_user должен сам захешировать пароль)
        user = User.objects.create_user(**validated_data)

        # создаем профиль
        Profile.objects.create(
            user=user,
            gender='M' if gender == 'male' else 'F',
            age=age,
            height=height,
            current_weight=weight,
            target_weight=weight,
            activity_level='sedentary',
            goal='maintain',
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    # читаем/пишем поля профиля через source
    height = serializers.FloatField(source='profile.height', required=False)
    weight = serializers.FloatField(source='profile.current_weight', required=False)
    gender = serializers.CharField(source='profile.gender', required=False)
    age = serializers.IntegerField(source='profile.age', required=False)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'avatar', 'created_at',
            'height', 'weight', 'gender', 'age',
        )
        read_only_fields = ('id', 'created_at')

    def update(self, instance, validated_data):
        from profiles.models import Profile

        profile_data = validated_data.pop('profile', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile, _ = Profile.objects.get_or_create(user=instance)

        if 'height' in profile_data:
            profile.height = profile_data['height']

        if 'current_weight' in profile_data:
            profile.current_weight = profile_data['current_weight']

        if 'gender' in profile_data:
            profile.gender = profile_data['gender']

        if 'age' in profile_data:
            profile.age = profile_data['age']

        profile.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
