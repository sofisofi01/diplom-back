from django.urls import path
from .views import (
    ExerciseListView, ExerciseDetailView,
    WorkoutPlanListCreateView, WorkoutPlanDetailView,
    WorkoutDayListCreateView, WorkoutExerciseListCreateView
)

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise-list'),
    path('<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('plans/', WorkoutPlanListCreateView.as_view(), name='workout-plan-list'),
    path('plans/<int:pk>/', WorkoutPlanDetailView.as_view(), name='workout-plan-detail'),
    path('plans/<int:plan_id>/days/', WorkoutDayListCreateView.as_view(), name='workout-day-list'),
    path('days/<int:day_id>/exercises/', WorkoutExerciseListCreateView.as_view(), name='workout-exercise-list'),
]
