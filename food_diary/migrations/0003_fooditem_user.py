from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food_diary', '0002_nutrition_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_food_items', to=settings.AUTH_USER_MODEL),
        ),
    ]
