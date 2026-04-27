from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('food_diary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='My Nutrition Plan', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nutrition_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='food_diary.nutritionplan')),
            ],
            options={
                'ordering': ['day_number'],
                'unique_together': {('plan', 'day_number')},
            },
        ),
        migrations.CreateModel(
            name='NutritionEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=255)),
                ('calories', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbs', models.FloatField(default=0)),
                ('fat', models.FloatField(default=0)),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack')], max_length=20)),
                ('is_eaten', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('nutrition_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='food_diary.nutritionday')),
            ],
        ),
    ]
