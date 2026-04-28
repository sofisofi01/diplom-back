from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('food_diary', '0003_fooditem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='meal_type',
            field=models.CharField(default='Breakfast', max_length=20),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='ingredients',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='recipe',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='cooking_time',
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nutritionentry',
            name='ingredients',
            field=models.TextField(blank=True, null=True),
        ),
    ]
