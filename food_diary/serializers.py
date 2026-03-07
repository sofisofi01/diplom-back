from rest_framework import serializers
from .models import FoodItem, FoodDiaryEntry


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'calories', 'protein', 'carbs', 'fat', 'serving_size')


class FoodDiaryEntrySerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    food_item_id = serializers.IntegerField(write_only=True)
    total_calories = serializers.FloatField(read_only=True)

    class Meta:
        model = FoodDiaryEntry
        fields = ('id', 'food_item', 'food_item_id', 'meal_type', 'servings', 'date', 'total_calories', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
