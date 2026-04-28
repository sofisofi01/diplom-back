from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import AIAssistantService
from food_diary.models import NutritionPlan
from food_diary.serializers import NutritionPlanSerializer
from exercises.models import WorkoutPlan
from exercises.serializers import WorkoutPlanSerializer

class AIAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Собираем данные о питании
        nutrition_plan = NutritionPlan.objects.filter(user=user, is_active=True).first()
        nutrition_data = NutritionPlanSerializer(nutrition_plan).data if nutrition_plan else []
        
        # Собираем данные о тренировках
        workout_plan = WorkoutPlan.objects.filter(user=user, is_active=True).first()
        workout_data = WorkoutPlanSerializer(workout_plan).data if workout_plan else []
        
        user_data = {
            'profile': {
                'current_weight': getattr(user.profile, 'current_weight', None),
                'target_weight': getattr(user.profile, 'target_weight', None),
                'goal': getattr(user.profile, 'goal', None),
            },
            'nutrition': nutrition_data.get('days', []) if isinstance(nutrition_data, dict) else [],
            'workouts': workout_data.get('days', []) if isinstance(workout_data, dict) else []
        }
        
        analysis = AIAssistantService.analyze_user_data(user_data)
        return Response(analysis)
