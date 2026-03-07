from django.urls import path
from .views import (
    WeightEntryListCreateView, 
    WeightEntryDetailView, 
    GoalProgressListCreateView,
    GoalProgressDetailView,
    ProgressAnalyticsView
)

urlpatterns = [
    path('weight/', WeightEntryListCreateView.as_view(), name='weight-entry-list'),
    path('weight/<int:pk>/', WeightEntryDetailView.as_view(), name='weight-entry-detail'),
    path('goals/', GoalProgressListCreateView.as_view(), name='goal-progress-list'),
    path('goals/<int:pk>/', GoalProgressDetailView.as_view(), name='goal-progress-detail'),
    path('analytics/', ProgressAnalyticsView.as_view(), name='progress-analytics'),
]
