from rest_framework import serializers
from .models import WeightEntry, GoalProgress


class WeightEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ('id', 'weight', 'date', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GoalProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    estimated_completion = serializers.SerializerMethodField()
    
    class Meta:
        model = GoalProgress
        fields = ('id', 'start_weight', 'target_weight', 'start_date', 'target_date', 
                 'is_active', 'progress_percentage', 'estimated_completion', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_progress_percentage(self, obj):
        return obj.calculate_progress_percentage()
    
    def get_estimated_completion(self, obj):
        return obj.estimate_completion_date()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
