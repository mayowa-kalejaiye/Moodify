# Generated migration for behavior engine fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        # Add behavior engine fields to Profile model
        migrations.AddField(
            model_name='profile',
            name='coin_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='clarity_score',
            field=models.PositiveSmallIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='streak_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_mood_log',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='streak_last_updated',
            field=models.DateField(blank=True, null=True),
        ),
        
        # Create Challenge model
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge_type', models.CharField(choices=[('daily_log', 'Daily Mood Log'), ('weekly_reflection', 'Weekly Reflection'), ('meditation_streak', 'Meditation Streak'), ('exercise_habit', 'Exercise Habit'), ('gratitude_practice', 'Gratitude Practice')], max_length=20)),
                ('stake', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('settled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='tracker.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        
        # Create CoinTransaction model
        migrations.CreateModel(
            name='CoinTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('earn_mood', 'Mood Log Reward'), ('earn_comment', 'Comment Reward'), ('earn_feedback', 'AI Feedback Reward'), ('earn_challenge', 'Challenge Completion'), ('spend_stake', 'Challenge Stake'), ('spend_insight', 'AI Insight Purchase'), ('lose_inactive', 'Inactivity Penalty')], max_length=20)),
                ('amount', models.IntegerField()),
                ('balance_after', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='tracker.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        
        # Create Nudge model
        migrations.CreateModel(
            name='Nudge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nudge_type', models.CharField(choices=[('time_reminder', 'Time Reminder'), ('mood_trend', 'Mood Trend Alert'), ('skip_pattern', 'Skip Pattern Warning'), ('achievement', 'Achievement Celebration'), ('support', 'Support Message')], max_length=20)),
                ('message', models.TextField()),
                ('tone', models.CharField(choices=[('professional', 'Professional'), ('gen_z', 'Gen Z Casual')], max_length=15)),
                ('viewed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nudges', to='tracker.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
