from django.contrib import admin
from .models import FoodItem, NutritionPlan, NutritionDay, NutritionEntry

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fat', 'serving_size')
    search_fields = ('name',)

@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'name')

@admin.register(NutritionDay)
class NutritionDayAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'day_number')
    list_filter = ('day_number',)

@admin.register(NutritionEntry)
class NutritionEntryAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'nutrition_day', 'meal_type', 'calories', 'is_eaten')
    list_filter = ('meal_type', 'is_eaten')
    search_fields = ('food_name',)
