from django.contrib import admin
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_muscles', 'difficulty')
    list_filter = ('difficulty', 'target_muscles')
    search_fields = ('name', 'description')

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__email')

@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ('plan', 'day_number', 'name')
    list_filter = ('plan',)

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('workout_day', 'exercise', 'sets', 'reps', 'order')
    list_filter = ('workout_day',)
