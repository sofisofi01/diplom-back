import requests
import json
import uuid
import os
import urllib3

# Отключаем предупреждения о небезопасном соединении (для GigaChat API)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AIAssistantService:
    @staticmethod
    def get_gigachat_token():
        """Получение токена авторизации GigaChat"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        # Эти данные должны быть в .env
        auth_data = os.getenv('GIGACHAT_CREDENTIALS')
        if not auth_data:
            print("GigaChat Error: GIGACHAT_CREDENTIALS not found in environment")
            return None
        
        payload = {'scope': 'GIGACHAT_API_PERS'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {auth_data}',
            'RqUID': str(uuid.uuid4())
        }

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            if response.status_code != 200:
                print(f"GigaChat Auth Error: Status {response.status_code}, Body: {response.text}")
                return None
            return response.json().get('access_token')
        except Exception as e:
            print(f"GigaChat Auth Exception: {e}")
            return None

    @staticmethod
    def analyze_user_data(user_data):
        token = AIAssistantService.get_gigachat_token()
        
        if not token:
            return AIAssistantService.local_fallback_analysis(user_data)
        
        profile = user_data.get('profile', {})
        
        # Логируем количество полученных данных
        print(f"AI Analysis Debug: Nutrition days: {len(user_data.get('nutrition', []))}, Workout days: {len(user_data.get('workouts', []))}", flush=True)
        
        # Очищаем данные от лишнего веса для API (413 Request Entity Too Large)
        weight_history = user_data.get('weight_history', [])[:3]
        
        nutrition_raw = user_data.get('nutrition', [])[:2]
        nutrition_summary = []
        for day in nutrition_raw:
            day_info = {"day": day.get('day_number'), "meals": [], "total_calories": 0}
            for entry in day.get('entries', []):
                cals = entry.get('calories') or 0
                day_info["meals"].append({
                    "name": entry.get('food_name') or entry.get('name'),
                    "calories": cals
                })
                day_info["total_calories"] += cals
            nutrition_summary.append(day_info)

        workouts_raw = user_data.get('workouts', [])[:2]
        workouts_summary = []
        for day in workouts_raw:
            day_info = {"day": day.get('day_number'), "exercises": []}
            for work_ex in day.get('exercises', []):
                ex_data = work_ex.get('exercise', {})
                ex_name = ex_data.get('name') if isinstance(ex_data, dict) else "Упражнение"
                
                # Добавляем детали: подходы, повторения, вес
                sets = work_ex.get('sets')
                reps = work_ex.get('reps')
                weight = work_ex.get('weight')
                
                details = []
                if sets: details.append(f"{sets} подх.")
                if reps: details.append(f"{reps} повт.")
                if weight: details.append(f"{weight} кг")
                
                full_ex_name = ex_name
                if details:
                    full_ex_name += f" ({', '.join(details)})"
                
                day_info["exercises"].append(full_ex_name)
            workouts_summary.append(day_info)
        
        # Формируем максимально компактный, но информативный текстовый контекст
        context = f"Цель: {profile.get('goal')}. Вес: сейчас {profile.get('current_weight')}, цель {profile.get('target_weight')}.\n"
        
        if weight_history:
            context += f"История веса: {', '.join([str(w.get('weight')) for w in weight_history])}.\n"
        
        if nutrition_summary:
            nutrition_parts = []
            for d in nutrition_summary:
                meals_str = ", ".join([f"{m['name']} ({m['calories']} ккал)" for m in d['meals'] if m['name']])
                if meals_str:
                    nutrition_parts.append(f"День {d['day']} (всего {d['total_calories']} ккал): {meals_str}")
            
            if nutrition_parts:
                context += "Питание: " + "; ".join(nutrition_parts) + ".\n"
            else:
                context += "Данные о приемах пищи отсутствуют.\n"
            
        if workouts_summary:
            workout_parts = []
            for d in workouts_summary:
                ex_str = ", ".join([ex for ex in d['exercises'] if ex])
                if ex_str:
                    workout_parts.append(f"День {d['day']}: {ex_str}")
            
            if workout_parts:
                context += "Тренировки: " + "; ".join(workout_parts) + "."
            else:
                context += "Данные об упражнениях отсутствуют."
        else:
            context += "Данные о тренировках отсутствуют."

        print(f"AI Analysis Debug: Context sent to GigaChat: {context}", flush=True)

        if not token:
            # Fallback к локальной логике, если API недоступно
            return AIAssistantService.local_fallback_analysis(user_data)

        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        
        prompt = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — профессиональный фитнес-тренер и нутрициолог. Проанализируй данные пользователя и дай краткую сводку, детальный анализ и 3 конкретных рекомендации. Ответ верни СТРОГО в формате JSON с полями: summary, detailed_analysis, recommendations (массив строк), status."
                },
                {
                    "role": "user",
                    "content": f"Проанализируй мои данные: {context}"
                }
            ],
            "temperature": 0.7
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(prompt), verify=False, timeout=30)
            
            # Логируем для отладки
            if response.status_code != 200:
                print(f"GigaChat API Error: Status {response.status_code}, Content: {response.text[:200]}")
                return AIAssistantService.local_fallback_analysis(user_data)
            
            response_text = response.text
            if not response_text:
                print("GigaChat API Error: Empty response body")
                return AIAssistantService.local_fallback_analysis(user_data)

            try:
                result = response.json()
            except json.JSONDecodeError as e:
                print(f"GigaChat API JSON Error: {e}. Body: {response_text[:200]}")
                return AIAssistantService.local_fallback_analysis(user_data)

            content = result['choices'][0]['message']['content']
            
            # Пытаемся распарсить JSON из ответа нейросети
            try:
                # Очищаем ответ от возможных markdown-тегов
                clean_content = content.strip()
                if clean_content.startswith("```json"):
                    clean_content = clean_content[7:]
                if clean_content.endswith("```"):
                    clean_content = clean_content[:-3]
                clean_content = clean_content.strip()
                
                return json.loads(clean_content)
            except:
                # Если нейросеть вернула текст вместо JSON, оборачиваем его
                return {
                    "summary": "Анализ готов",
                    "detailed_analysis": content,
                    "recommendations": ["Следуйте советам выше"],
                    "status": "On Track"
                }
        except Exception as e:
            print(f"GigaChat API Error: {e}")
            return AIAssistantService.local_fallback_analysis(user_data)

    @staticmethod
    def local_fallback_analysis(user_data):
        # Наша старая добрая локальная логика на случай сбоя API
        profile = user_data.get('profile', {})
        target_weight = profile.get('target_weight')
        current_weight = profile.get('current_weight')
        
        analysis_parts = ["Локальный анализ (API временно недоступен):"]
        if target_weight and current_weight:
            diff = current_weight - target_weight
            analysis_parts.append(f"До цели осталось {diff:.1f} кг.")
        
        return {
            "summary": "Ваш прогресс анализируется локально.",
            "detailed_analysis": "\n\n".join(analysis_parts),
            "recommendations": [
                "Пейте больше воды",
                "Соблюдайте режим сна",
                "Не пропускайте тренировки"
            ],
            "status": "On Track"
        }
