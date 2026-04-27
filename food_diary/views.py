from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from datetime import datetime
import requests
from .models import FoodItem, FoodDiaryEntry
from .serializers import FoodItemSerializer, FoodDiaryEntrySerializer
from wellness_backend.cache_service import CacheService


class FoodSearchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Параметр q обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        cached_result = CacheService.get_food_search_cache(query)
        if cached_result:
            return Response(cached_result)
        
        try:
            results = self._search_usda(query)
            CacheService.set_food_search_cache(query, results)
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _search_usda(self, query):
        """Поиск через Open Food Facts (бесплатный, без API ключа)"""
        url = 'https://world.openfoodfacts.org/cgi/search.pl'
        params = {
            'search_terms': query,
            'page_size': 10,
            'json': 1,
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('products', []):
            nutrients = item.get('nutriments', {})
            results.append({
                'name': item.get('product_name', item.get('product_name_en', 'Unknown')),
                'calories': nutrients.get('energy-kcal_100g', 0),
                'protein': nutrients.get('proteins_100g', 0),
                'carbs': nutrients.get('carbohydrates_100g', 0),
                'fat': nutrients.get('fat_100g', 0),
                'external_id': item.get('code', ''),
            })
        return results


class FoodDiaryEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodDiaryEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = FoodDiaryEntry.objects.filter(user=self.request.user)
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset


class FoodDiaryEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodDiaryEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FoodDiaryEntry.objects.filter(user=self.request.user)


class DailyCaloriesSummaryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date = request.query_params.get('date', datetime.now().date())
        entries = FoodDiaryEntry.objects.filter(user=request.user, date=date)
        
        total_calories = sum(entry.total_calories() for entry in entries)
        
        by_meal = {}
        for meal_type, _ in FoodDiaryEntry.MEAL_CHOICES:
            meal_entries = entries.filter(meal_type=meal_type)
            by_meal[meal_type] = sum(entry.total_calories() for entry in meal_entries)
        
        return Response({
            'date': date,
            'total_calories': total_calories,
            'by_meal': by_meal,
        })


from .models import FoodItem, NutritionPlan, NutritionDay, NutritionEntry
from .serializers import FoodItemSerializer, NutritionPlanSerializer, NutritionEntrySerializer
from django.shortcuts import get_object_or_404


class ActiveNutritionPlanView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        plan = NutritionPlan.objects.filter(user=request.user, is_active=True).first()
        if not plan:
            plan = NutritionPlan.objects.create(user=request.user)
            for i in range(1, 8):
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                NutritionDay.objects.create(plan=plan, day_number=i, name=day_names[i-1])
        
        serializer = NutritionPlanSerializer(plan)
        return Response(serializer.data)


class AddFoodToPlanView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        day_number = request.data.get('day_number')
        meal_type = request.data.get('meal_type')
        food_name = request.data.get('food_name')
        calories = request.data.get('calories', 0)
        protein = request.data.get('protein', 0)
        carbs = request.data.get('carbs', 0)
        fat = request.data.get('fat', 0)
        image_url = request.data.get('image_url')

        plan = NutritionPlan.objects.filter(user=request.user, is_active=True).first()
        if not plan:
            return Response({"error": "No active plan found"}, status=status.HTTP_404_NOT_FOUND)

        nutrition_day = get_object_or_404(NutritionDay, plan=plan, day_number=day_number)

        entry = NutritionEntry.objects.create(
            nutrition_day=nutrition_day,
            food_name=food_name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            meal_type=meal_type,
            image_url=image_url
        )

        return Response(NutritionEntrySerializer(entry).data, status=status.HTTP_201_CREATED)


class NutritionEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NutritionEntry.objects.all()
    serializer_class = NutritionEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return NutritionEntry.objects.filter(nutrition_day__plan__user=self.request.user)
