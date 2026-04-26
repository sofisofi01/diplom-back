from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    height = serializers.FloatField(required=False)
    weight = serializers.FloatField(required=False)
    gender = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    activity_level = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 
                  'height', 'weight', 'gender', 'birth_date', 'activity_level')

    def create(self, validated_data):
        from profiles.models import Profile
        from datetime import date
        
        # Извлекаем данные профиля
        height = validated_data.pop('height', 170)
        weight = validated_data.pop('weight', 70)
        gender = validated_data.pop('gender', 'male')
        birth_date = validated_data.pop('birth_date', None)
        activity_level_idx = validated_data.pop('activity_level', 1)
        
        # Создаем пользователя
        user = User.objects.create_user(**validated_data)
        
        # Рассчитываем возраст
        age = 25
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Маппинг активности
        activity_map = {1: 'sedentary', 2: 'light', 3: 'moderate', 4: 'active', 5: 'very_active'}
        activity_level = activity_map.get(activity_level_idx, 'sedentary')
        
        # Создаем профиль
        Profile.objects.create(
            user=user,
            gender='M' if gender == 'male' else 'F',
            age=age,
            height=height,
            current_weight=weight,
            target_weight=weight, # По умолчанию цель - текущий вес
            activity_level=activity_level,
            goal='maintain'
        )
        
        return user



class UserSerializer(serializers.ModelSerializer):
    height = serializers.FloatField(source='profile.height', required=False)
    weight = serializers.FloatField(source='profile.current_weight', required=False)
    gender = serializers.CharField(source='profile.gender', required=False)
    age = serializers.IntegerField(source='profile.age', required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'created_at',
                  'height', 'weight', 'gender', 'age')
        read_only_fields = ('id', 'created_at')

    def update(self, instance, validated_data):
        from profiles.models import Profile
        profile_data = validated_data.pop('profile', {})
        
        # Обновляем поля самого пользователя
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем поля профиля
        profile, _ = Profile.objects.get_or_create(user=instance)
        if 'height' in profile_data: profile.height = profile_data['height']
        if 'current_weight' in profile_data: profile.current_weight = profile_data['current_weight']
        if 'gender' in profile_data: profile.gender = profile_data['gender']
        if 'age' in profile_data: profile.age = profile_data['age']
        profile.save()

        return instance


    def update(self, instance, validated_data):
        from profiles.models import Profile
        
        # Данные профиля
        height = validated_data.pop('height', None)
        weight = validated_data.pop('weight', None)
        gender = validated_data.pop('gender', None)
        age = validated_data.pop('age', None)

        # Обновляем поля пользователя
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем или создаем профиль
        profile, created = Profile.objects.get_or_create(user=instance)
        if height is not None: profile.height = height
        if weight is not None: profile.current_weight = weight
        if gender is not None: profile.gender = 'M' if gender == 'male' else 'F'
        if age is not None: profile.age = age
        profile.save()

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
