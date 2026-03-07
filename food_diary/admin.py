from django.contrib import admin
from .models import FoodItem, FoodDiaryEntry

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fat', 'serving_size')
    search_fields = ('name',)

@admin.register(FoodDiaryEntry)
class FoodDiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'meal_type', 'servings', 'date')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__email', 'food_item__name')
