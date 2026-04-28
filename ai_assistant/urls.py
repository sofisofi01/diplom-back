from django.urls import path
from .views import AIAnalysisView

urlpatterns = [
    path('analysis/', AIAnalysisView.as_view(), name='ai-analysis'),
]
