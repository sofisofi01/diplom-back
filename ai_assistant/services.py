import requests
import json
import uuid
import os

class AIAssistantService:
    @staticmethod
    def get_gigachat_token():
        """Получение токена авторизации GigaChat"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        # Эти данные должны быть в .env, пока используем заглушку для структуры
        auth_data = os.getenv('GIGACHAT_CREDENTIALS', 'YOUR_GIGACHAT_CREDENTIALS_BASE64')
        
        payload = {'scope': 'GIGACHAT_API_PERS'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {auth_data}',
            'RqUID': str(uuid.uuid4())
        }

        try:
            # verify=False так как у Сбера часто самоподписанные сертификаты в API
            response = requests.post(url, headers=headers, data=payload, verify=False)
            return response.json().get('access_token')
        except Exception as e:
            print(f"GigaChat Auth Error: {e}")
            return None

    @staticmethod
    def analyze_user_data(user_data):
        token = AIAssistantService.get_gigachat_token()
        
        profile = user_data.get('profile', {})
        nutrition = user_data.get('nutrition', [])
        workouts = user_data.get('workouts', [])
        weight_history = user_data.get('weight_history', [])
        
        # Формируем контекст для нейросети
        context = f"""
        User Profile:
        - Current Weight: {profile.get('current_weight')}kg
        - Target Weight: {profile.get('target_weight')}kg
        - Goal: {profile.get('goal')}
        
        Weight History (last entries):
        {json.dumps(weight_history, indent=2)}
        
        Nutrition Data (last plan):
        {json.dumps(nutrition, indent=2)}
        
        Workout Data:
        {json.dumps(workouts, indent=2)}
        """

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
            response = requests.post(url, headers=headers, data=json.dumps(prompt), verify=False)
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Пытаемся распарсить JSON из ответа нейросети
            try:
                return json.loads(content)
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
