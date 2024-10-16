# Generated by Django 5.1.2 on 2024-10-15 17:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_mood_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='mood',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mood',
            name='sentiment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mood',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
