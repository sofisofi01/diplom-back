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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ActiveWorkoutPlanView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        plan = WorkoutPlan.objects.filter(user=request.user, is_active=True).first()
        if not plan:
            # Создаем план по умолчанию, если его нет
            plan = WorkoutPlan.objects.create(
                user=request.user,
                name="My Workout Plan",
                is_active=True
            )
            # Создаем 7 дней
            for i in range(1, 8):
                WorkoutDay.objects.create(plan=plan, day_number=i, name=f"Day {i}")
        
        serializer = WorkoutPlanSerializer(plan)
        return Response(serializer.data)

class AddExerciseToPlanView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        day_number = request.data.get('day_number')
        exercise_id = request.data.get('exercise_id')
        sets = request.data.get('sets', 3)
        reps = request.data.get('reps', 10)

        plan = WorkoutPlan.objects.filter(user=request.user, is_active=True).first()
        if not plan:
            return Response({"error": "No active plan found"}, status=status.HTTP_404_NOT_FOUND)

        workout_day = get_object_or_404(WorkoutDay, plan=plan, day_number=day_number)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        workout_exercise = WorkoutExercise.objects.create(
            workout_day=workout_day,
            exercise=exercise,
            sets=sets,
            reps=reps,
            order=workout_day.exercises.count()
        )

        return Response(WorkoutExerciseSerializer(workout_exercise).data, status=status.HTTP_201_CREATED)

class WorkoutExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return WorkoutExercise.objects.filter(workout_day__plan__user=self.request.user)
