from django.db import models
from django.conf import settings
from datetime import datetime, timedelta


class WeightEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weight_entries')
    weight = models.FloatField(help_text='Вес в кг')
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name_plural = 'Weight entries'

    def __str__(self):
        return f"{self.user.email} - {self.weight}кг - {self.date}"


class GoalProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goal_progress')
    start_weight = models.FloatField()
    target_weight = models.FloatField()
    start_date = models.DateField()
    target_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_progress_percentage(self):
        """Рассчитывает процент достижения цели"""
        latest_weight = self.user.weight_entries.first()
        if not latest_weight:
            return 0
        
        total_change_needed = abs(self.target_weight - self.start_weight)
        current_change = abs(latest_weight.weight - self.start_weight)
        
        if total_change_needed == 0:
            return 100
        
        progress = (current_change / total_change_needed) * 100
        return min(progress, 100)

    def estimate_completion_date(self):
        """Прогнозирует дату достижения цели"""
        weight_entries = self.user.weight_entries.filter(date__gte=self.start_date).order_by('date')
        
        if len(weight_entries) < 2:
            return None
        
        # Используем количество дней от первой записи как X для корректного наклона
        first_date = weight_entries[0].date
        x = [(entry.date - first_date).days for entry in weight_entries]
        y = [entry.weight for entry in weight_entries]
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        
        denominator = (n * sum_x2 - sum_x * sum_x)
        if denominator == 0:
            return None
            
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        # Проверяем, движемся ли мы к цели
        is_losing = self.target_weight < self.start_weight
        if (is_losing and slope >= 0) or (not is_losing and slope <= 0):
            return None # Прогноз невозможен при такой динамике
            
        current_weight = y[-1]
        weight_to_go = self.target_weight - current_weight
        days_needed = weight_to_go / slope
        
        if days_needed <= 0:
            return datetime.now().date()
            
        # Ограничиваем прогноз разумными пределами (2 года)
        if days_needed > 730:
            return None
            
        return weight_entries.last().date + timedelta(days=int(days_needed))

    def __str__(self):
        return f"{self.user.email} - цель: {self.target_weight}кг"
