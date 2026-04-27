from django.urls import path
from .views import (
    FoodSearchView, FoodDiaryEntryListCreateView, 
    FoodDiaryEntryDetailView, DailyCaloriesSummaryView, 
    ActiveNutritionPlanView, AddFoodToPlanView, NutritionEntryDetailView
)

urlpatterns = [
    path('search/', FoodSearchView.as_view(), name='food-search'),
    path('entries/', FoodDiaryEntryListCreateView.as_view(), name='diary-entries'),
    path('entries/<int:pk>/', FoodDiaryEntryDetailView.as_view(), name='diary-entry-detail'),
    path('summary/', DailyCaloriesSummaryView.as_view(), name='daily-summary'),
    path('plans/active/', ActiveNutritionPlanView.as_view(), name='active-nutrition-plan'),
    path('plans/add_food/', AddFoodToPlanView.as_view(), name='add-food-to-plan'),
    path('nutrition-entries/<int:pk>/', NutritionEntryDetailView.as_view(), name='nutrition-entry-detail'),
]
