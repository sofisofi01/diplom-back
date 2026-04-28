class AIAssistantService:
    @staticmethod
    def analyze_user_data(user_data):
        profile = user_data.get('profile', {})
        nutrition = user_data.get('nutrition', [])
        workouts = user_data.get('workouts', [])
        
        target_weight = profile.get('target_weight')
        current_weight = profile.get('current_weight')
        
        analysis_parts = []
        
        # Анализ веса
        if target_weight and current_weight:
            diff = current_weight - target_weight
            if diff > 0:
                analysis_parts.append(f"You are {diff:.1f}kg away from your goal. Your current progress is visible, but consistency in nutrition is key.")
            elif diff < 0:
                analysis_parts.append(f"You are {abs(diff):.1f}kg below your target. Ensure you are consuming enough calories for healthy maintenance or muscle growth.")
            else:
                analysis_parts.append("You have reached your target weight! Excellent work on maintaining your goals.")
        
        # Анализ питания
        total_meals = sum(len(day.get('entries', [])) for day in nutrition)
        if total_meals == 0:
            analysis_parts.append("You haven't logged any meals in your current plan. Tracking your food intake will help me provide more accurate advice.")
        else:
            eaten_meals = sum(1 for day in nutrition for entry in day.get('entries', []) if entry.get('is_eaten'))
            if eaten_meals > 0:
                analysis_parts.append(f"You've logged {eaten_meals} meals as eaten. This data helps in tracking your actual calorie intake.")
            else:
                analysis_parts.append("You have a nutrition plan, but haven't marked any meals as eaten yet.")
            
        # Анализ тренировок
        if not workouts:
            analysis_parts.append("I don't see any active workout plans. Regular physical activity is crucial for both physical and mental well-being.")
        else:
            analysis_parts.append(f"You have an active workout plan with {len(workouts)} days of exercises. Make sure to balance intensity with recovery.")
            
        detailed_analysis = "\n\n".join(analysis_parts)
        
        recommendations = [
            "Drink at least 2 liters of water daily to support metabolism.",
            "Prioritize 7-8 hours of sleep for optimal recovery.",
            "Include more fiber-rich vegetables in your lunch and dinner."
        ]
        
        if not workouts:
            recommendations.append("Start with 20-minute light walks daily.")
        
        return {
            "summary": "Your journey is unique. Based on your current data, you are making progress, but there's room for optimization in tracking and consistency.",
            "detailed_analysis": detailed_analysis,
            "recommendations": recommendations,
            "status": "Analyzing" if not total_meals else "On Track"
        }
