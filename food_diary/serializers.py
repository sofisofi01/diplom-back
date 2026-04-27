from rest_framework import serializers
from .models import FoodItem, NutritionPlan, NutritionDay, NutritionEntry


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'calories', 'protein', 'carbs', 'fat', 'serving_size')


class NutritionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionEntry
        fields = ('id', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'meal_type', 'is_eaten', 'image_url')


class NutritionDaySerializer(serializers.ModelSerializer):
    entries = NutritionEntrySerializer(many=True, read_only=True)

    class Meta:
        model = NutritionDay
        fields = ('id', 'day_number', 'name', 'entries')


class NutritionPlanSerializer(serializers.ModelSerializer):
    days = NutritionDaySerializer(many=True, read_only=True)

    class Meta:
        model = NutritionPlan
        fields = ('id', 'name', 'is_active', 'days', 'created_at')
