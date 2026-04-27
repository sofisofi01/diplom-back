from django.urls import path
from .views import (
    FoodSearchView, ActiveNutritionPlanView, 
    AddFoodToPlanView, NutritionEntryDetailView
)

urlpatterns = [
    path('search/', FoodSearchView.as_view(), name='food-search'),
    path('plans/active/', ActiveNutritionPlanView.as_view(), name='active-nutrition-plan'),
    path('plans/add_food/', AddFoodToPlanView.as_view(), name='add-food-to-plan'),
    path('nutrition-entries/<int:pk>/', NutritionEntryDetailView.as_view(), name='nutrition-entry-detail'),
]
