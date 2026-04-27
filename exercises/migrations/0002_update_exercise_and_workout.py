from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='exercise',
        #     name='calories_per_repetition',
        #     field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        # ),
        # migrations.AddField(
        #     model_name='exercise',
        #     name='equipment',
        #     field=models.JSONField(default=list, help_text='Список необходимого оборудования'),
        # ),
        migrations.AddField(
            model_name='workoutexercise',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        # migrations.AlterField(
        #     model_name='exercise',
        #     name='target_muscles',
        #     field=models.JSONField(default=list, help_text='Список целевых мышц'),
        # ),
    ]
