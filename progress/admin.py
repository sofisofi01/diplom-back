from django.contrib import admin
from .models import WeightEntry, GoalProgress

@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-date',)


@admin.register(GoalProgress)
class GoalProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_weight', 'target_weight', 'start_date', 'target_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'target_date')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
