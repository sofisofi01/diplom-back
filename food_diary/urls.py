from django.urls import path
from .views import (
    FoodSearchView, FoodDiaryEntryListCreateView, 
    FoodDiaryEntryDetailView, DailyCaloriesSummaryView, CreateFoodItemView
)

urlpatterns = [
    path('search/', FoodSearchView.as_view(), name='food-search'),
    path('entries/', FoodDiaryEntryListCreateView.as_view(), name='diary-entries'),
    path('entries/<int:pk>/', FoodDiaryEntryDetailView.as_view(), name='diary-entry-detail'),
    path('summary/', DailyCaloriesSummaryView.as_view(), name='daily-summary'),
    path('food-items/', CreateFoodItemView.as_view(), name='create-food-item'),
]
