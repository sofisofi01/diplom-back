from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'gender', 'age', 'height', 'current_weight', 'target_weight', 
                  'activity_level', 'goal', 'daily_calories', 'created_at', 'updated_at')
        read_only_fields = ('id', 'daily_calories', 'created_at', 'updated_at')
