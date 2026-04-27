from django.urls import path
from .views import (
    ExerciseListView, ExerciseDetailView,
    WorkoutPlanListCreateView, WorkoutPlanDetailView,
    WorkoutDayListCreateView, ActiveWorkoutPlanView,
    AddExerciseToPlanView, WorkoutExerciseDetailView
)

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise-list'),
    path('<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('plans/', WorkoutPlanListCreateView.as_view(), name='workout-plan-list'),
    path('plans/active/', ActiveWorkoutPlanView.as_view(), name='active-plan'),
    path('plans/add_exercise/', AddExerciseToPlanView.as_view(), name='add-exercise-to-plan'),
    path('plans/<int:pk>/', WorkoutPlanDetailView.as_view(), name='workout-plan-detail'),
    path('plans/<int:plan_id>/days/', WorkoutDayListCreateView.as_view(), name='workout-day-list'),
    path('workout-exercises/<int:pk>/', WorkoutExerciseDetailView.as_view(), name='workout-exercise-detail'),
]
