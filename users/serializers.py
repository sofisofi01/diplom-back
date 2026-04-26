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
    height = serializers.FloatField(source='profile.height', read_only=True)
    weight = serializers.FloatField(source='profile.current_weight', read_only=True)
    gender = serializers.CharField(source='profile.gender', read_only=True)
    age = serializers.IntegerField(source='profile.age', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'created_at', 
                  'height', 'weight', 'gender', 'age')
        read_only_fields = ('id', 'created_at')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
