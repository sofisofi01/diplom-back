from rest_framework import serializers
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'target_muscles', 'equipment', 'calories_per_repetition', 'difficulty', 'image', 'video_url')


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    exercise_id = serializers.IntegerField(write_only=True)
    total_calories = serializers.ReadOnlyField()

    class Meta:
        model = WorkoutExercise
        fields = ('id', 'exercise', 'exercise_id', 'sets', 'reps', 'weight', 'rest_seconds', 'order', 'total_calories')


class WorkoutDaySerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutDay
        fields = ('id', 'plan', 'day_number', 'name', 'exercises')


class WorkoutPlanSerializer(serializers.ModelSerializer):
    days = WorkoutDaySerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ('id', 'name', 'description', 'is_active', 'days', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
