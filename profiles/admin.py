from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'current_weight', 'target_weight', 'goal', 'daily_calories')
    list_filter = ('gender', 'goal', 'activity_level')
    search_fields = ('user__email',)
