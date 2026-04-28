from django.db import models
from django.conf import settings


class FoodItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='custom_food_items')
    name = models.CharField(max_length=200)
    calories = models.FloatField()
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    serving_size = models.CharField(max_length=100)
    external_id = models.CharField(max_length=200, null=True, blank=True)
    meal_type = models.CharField(max_length=20, default="Breakfast")
    ingredients = models.TextField(blank=True, null=True)
    recipe = models.TextField(blank=True, null=True)
    cooking_time = models.IntegerField(default=15)
    image_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NutritionPlan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nutrition_plan')
    name = models.CharField(max_length=200, default="My Nutrition Plan")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"

class NutritionDay(models.Model):
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField() # 1-7
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['day_number']
        unique_together = ['plan', 'day_number']

    def __str__(self):
        return f"{self.plan.name} - {self.name}"

class NutritionEntry(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    nutrition_day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE, related_name='entries')
    food_name = models.CharField(max_length=255)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    is_eaten = models.BooleanField(default=False)
    image_url = models.URLField(null=True, blank=True)
    ingredients = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.food_name} ({self.meal_type})"
