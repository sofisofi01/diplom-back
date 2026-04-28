from django.db import models
from django.conf import settings


class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    MUSCLE_CHOICES = [
        ('deltoid', 'Deltoid'),
        ('abs', 'Abs'),
        ('chest', 'Chest'),
        ('legs', 'Legs'),
        ('back', 'Back muscles'),
        ('hands', 'Hands'),
        ('trapezoid', 'Trapezoid'),
        ('cardio', 'Cardio'),
        ('warm', 'Warm'),
    ]

    EQUIPMENT_CHOICES = [
        ('dumbbells', 'Dumbbells'),
        ('kettlebell', 'Kettlebell'),
        ('jump_rope', 'Jump rope'),
        ('resistance_band', 'Resistance band'),
        ('mat', 'Mat'),
        ('weights', 'Weights'),
        ('barbell', 'Barbell'),
        ('horizontal_bar', 'Horizontal bar'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    target_muscles = models.JSONField(
        default=list,
        help_text='Список целевых мышц'
    )
    equipment = models.JSONField(
        default=list,
        help_text='Список необходимого оборудования'
    )
    calories_per_repetition = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.0
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"


class WorkoutDay(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['day_number']
        unique_together = ['plan', 'day_number']

    def __str__(self):
        return f"{self.plan.name} - День {self.day_number}"


class WorkoutExercise(models.Model):
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField(null=True, blank=True, help_text='Вес в кг')
    rest_seconds = models.IntegerField(default=60)
    order = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    @property
    def total_calories(self):
        # Базовый расход на одно повторение (если не задано, берем 0.1 ккал как среднее)
        base_calories = float(self.exercise.calories_per_repetition) if self.exercise.calories_per_repetition else 0.1
        
        # Коэффициент веса отягощения
        weight_factor = 1.0
        if self.weight:
            # Каждые 10 кг веса добавляют примерно 5% к интенсивности
            weight_factor = 1.0 + (self.weight / 200.0)
            
        # Если это кардио (обычно reps > 30 или target_muscles содержит cardio), 
        # то reps может считаться как секунды. Но для простоты пока считаем по повторам.
        return round(base_calories * self.reps * self.sets * weight_factor, 2)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"
