from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('food_diary', '0004_fooditem_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionentry',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nutritionentry',
            name='recipe',
            field=models.TextField(blank=True, null=True),
        ),
    ]
