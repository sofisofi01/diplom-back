from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise
from .serializers import (
    ExerciseSerializer, WorkoutPlanSerializer, 
    WorkoutDaySerializer, WorkoutExerciseSerializer
)


class ExerciseListView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated,)


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated,)


class WorkoutPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutPlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)


class WorkoutPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutPlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)


class WorkoutDayListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutDaySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        plan_id = self.kwargs.get('plan_id')
        return WorkoutDay.objects.filter(plan_id=plan_id, plan__user=self.request.user)


class WorkoutExerciseListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutExerciseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        day_id = self.kwargs.get('day_id')
        return WorkoutExercise.objects.filter(workout_day_id=day_id, workout_day__plan__user=self.request.user)
