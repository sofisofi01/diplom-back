from django.db import models
from django.conf import settings


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    ACTIVITY_CHOICES = [
        ('sedentary', 'Сидячий образ жизни'),
        ('light', 'Легкая активность'),
        ('moderate', 'Умеренная активность'),
        ('active', 'Высокая активность'),
        ('very_active', 'Очень высокая активность'),
    ]
    
    GOAL_CHOICES = [
        ('lose', 'Похудение'),
        ('maintain', 'Поддержание веса'),
        ('gain', 'Набор массы'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text='Рост в см', null=True, blank=True)
    current_weight = models.FloatField(help_text='Текущий вес в кг', null=True, blank=True)
    target_weight = models.FloatField(help_text='Желаемый вес в кг', null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, null=True, blank=True)
    daily_calories = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_bmr(self):
        """Расчет базального метаболизма по формуле Миффлина-Сан Жеора"""
        if not all([self.current_weight, self.height, self.age]):
            return 0
            
        if self.gender == 'M':
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * self.age - 161
        return bmr

    def calculate_daily_calories(self):
        """Расчет суточной нормы калорий с учетом активности и цели"""
        bmr = self.calculate_bmr()
        if bmr == 0:
            return 0
            
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9,
        }
        
        tdee = bmr * activity_multipliers.get(self.activity_level, 1.2)
        
        if self.goal == 'lose':
            calories = tdee - 500
        elif self.goal == 'gain':
            calories = tdee + 500
        else:
            calories = tdee
        
        return int(calories)

    def save(self, *args, **kwargs):
        self.daily_calories = self.calculate_daily_calories()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Профиль {self.user.email}"
