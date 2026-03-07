from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from datetime import datetime, timedelta
from .models import WeightEntry, GoalProgress
from .serializers import WeightEntrySerializer, GoalProgressSerializer
from food_diary.models import FoodDiaryEntry


class WeightEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = WeightEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = WeightEntry.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset


class WeightEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WeightEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WeightEntry.objects.filter(user=self.request.user)


class GoalProgressListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalProgressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return GoalProgress.objects.filter(user=self.request.user)


class GoalProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalProgressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return GoalProgress.objects.filter(user=self.request.user)


class ProgressAnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now().date() - timedelta(days=days)
        
        weight_entries = WeightEntry.objects.filter(user=user, date__gte=start_date).order_by('date')
        weight_data = [{'date': entry.date, 'weight': entry.weight} for entry in weight_entries]
        
        food_entries = FoodDiaryEntry.objects.filter(user=user, date__gte=start_date)
        daily_calories = {}
        for entry in food_entries:
            date_str = str(entry.date)
            if date_str not in daily_calories:
                daily_calories[date_str] = 0
            daily_calories[date_str] += entry.total_calories()
        
        calories_data = [{'date': date, 'calories': calories} for date, calories in daily_calories.items()]
        
        profile = getattr(user, 'profile', None)
        target_weight = profile.target_weight if profile else None
        daily_calorie_goal = profile.daily_calories if profile else None
        
        weight_change = None
        if len(weight_entries) >= 2:
            weight_change = weight_entries.last().weight - weight_entries.first().weight
        
        avg_calories = sum(daily_calories.values()) / len(daily_calories) if daily_calories else 0
        
        # Анализ соответствия плану
        calorie_adherence = []
        if daily_calorie_goal:
            for date, calories in daily_calories.items():
                adherence = (calories / daily_calorie_goal) * 100
                calorie_adherence.append({'date': date, 'adherence': adherence})
        
        # Активная цель
        active_goal = GoalProgress.objects.filter(user=user, is_active=True).first()
        goal_data = None
        if active_goal:
            goal_data = {
                'progress_percentage': active_goal.calculate_progress_percentage(),
                'estimated_completion': active_goal.estimate_completion_date(),
                'target_weight': active_goal.target_weight,
                'start_weight': active_goal.start_weight
            }
        
        return Response({
            'weight_data': weight_data,
            'calories_data': calories_data,
            'calorie_adherence': calorie_adherence,
            'target_weight': target_weight,
            'daily_calorie_goal': daily_calorie_goal,
            'weight_change': weight_change,
            'avg_daily_calories': round(avg_calories, 2),
            'goal_progress': goal_data,
        })
