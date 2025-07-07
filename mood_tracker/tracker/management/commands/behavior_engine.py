"""
Management command to initialize and manage the MoodSync Behavior Engine
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from datetime import date, timedelta
import random

from mood_tracker.tracker.models import Profile, Challenge, CoinTransaction, Nudge, Mood


class Command(BaseCommand):
    help = 'Initialize and manage MoodSync Behavior Engine'

    def add_arguments(self, parser):
        parser.add_argument(
            '--init-profiles',
            action='store_true',
            help='Initialize behavior engine fields for existing profiles',
        )
        parser.add_argument(
            '--update-streaks',
            action='store_true',
            help='Update streaks for all users',
        )
        parser.add_argument(
            '--settle-challenges',
            action='store_true',
            help='Settle all completed challenges',
        )
        parser.add_argument(
            '--generate-demo-data',
            action='store_true',
            help='Generate demo data for testing',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Specify a particular user for operations',
        )

    def handle(self, *args, **options):
        if options['init_profiles']:
            self.init_profiles()
        
        if options['update_streaks']:
            self.update_streaks(options.get('user'))
        
        if options['settle_challenges']:
            self.settle_challenges(options.get('user'))
        
        if options['generate_demo_data']:
            self.generate_demo_data()
        
        if not any([options['init_profiles'], options['update_streaks'], 
                   options['settle_challenges'], options['generate_demo_data']]):
            self.print_help('manage.py', 'behavior_engine')

    def init_profiles(self):
        """Initialize behavior engine fields for existing profiles"""
        self.stdout.write('Initializing behavior engine for existing profiles...')
        
        profiles = Profile.objects.all()
        updated_count = 0
        
        for profile in profiles:
            updated = False
            
            # Set default values if not set
            if profile.coin_balance is None:
                profile.coin_balance = 0
                updated = True
            
            if profile.clarity_score is None:
                profile.clarity_score = 100
                updated = True
            
            if profile.streak_count is None:
                profile.streak_count = 0
                updated = True
            
            if updated:
                profile.save()
                updated_count += 1
                self.stdout.write(f'  Updated profile for {profile.user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully initialized {updated_count} profiles')
        )

    def update_streaks(self, username=None):
        """Update streaks for users"""
        self.stdout.write('Updating streaks...')
        
        if username:
            try:
                user = User.objects.get(username=username)
                profiles = [Profile.objects.get(user=user)]
            except (User.DoesNotExist, Profile.DoesNotExist):
                raise CommandError(f'User "{username}" not found')
        else:
            profiles = Profile.objects.all()
        
        updated_count = 0
        
        for profile in profiles:
            old_streak = profile.streak_count
            profile.update_streak()
            
            if profile.streak_count != old_streak:
                self.stdout.write(
                    f'  {profile.user.username}: {old_streak} -> {profile.streak_count}'
                )
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} streaks')
        )

    def settle_challenges(self, username=None):
        """Settle completed challenges"""
        self.stdout.write('Settling challenges...')
        
        if username:
            try:
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                challenges = Challenge.objects.filter(profile=profile, settled=False)
            except (User.DoesNotExist, Profile.DoesNotExist):
                raise CommandError(f'User "{username}" not found')
        else:
            challenges = Challenge.objects.filter(settled=False)
        
        settled_count = 0
        
        for challenge in challenges:
            if challenge.end_date < date.today():
                with transaction.atomic():
                    challenge.check_completion()
                    
                    if challenge.completed:
                        # Award coins
                        reward = challenge.stake * 2
                        challenge.profile.coin_balance += reward
                        challenge.profile.save()
                        
                        # Create transaction
                        CoinTransaction.objects.create(
                            profile=challenge.profile,
                            transaction_type='win_challenge',
                            amount=reward,
                            balance_after=challenge.profile.coin_balance,
                            challenge=challenge
                        )
                        
                        self.stdout.write(
                            f'  {challenge.profile.user.username} won challenge: +{reward} coins'
                        )
                    else:
                        self.stdout.write(
                            f'  {challenge.profile.user.username} lost challenge'
                        )
                    
                    challenge.settled = True
                    challenge.save()
                    settled_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully settled {settled_count} challenges')
        )

    def generate_demo_data(self):
        """Generate demo data for testing"""
        self.stdout.write('Generating demo data...')
        
        # Create demo user if not exists
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write('  Created demo user')
        
        # Set up profile
        profile = Profile.objects.get(user=demo_user)
        profile.age = 25
        profile.coin_balance = 50
        profile.clarity_score = 85
        profile.streak_count = 5
        profile.last_mood_log = date.today() - timedelta(days=1)
        profile.save()
        
        # Create some demo moods
        mood_data = [
            {'mood': 'happy', 'rating': 4, 'notes': 'Great day at work!'},
            {'mood': 'calm', 'rating': 3, 'notes': 'Relaxing evening'},
            {'mood': 'excited', 'rating': 5, 'notes': 'Got promoted!'},
            {'mood': 'stressed', 'rating': 2, 'notes': 'Busy day'},
            {'mood': 'content', 'rating': 4, 'notes': 'Nice weekend'},
        ]
        
        for i, mood_info in enumerate(mood_data):
            mood_date = timezone.now() - timedelta(days=i)
            mood, created = Mood.objects.get_or_create(
                user=demo_user,
                created_at=mood_date,
                defaults=mood_info
            )
            if created:
                self.stdout.write(f'  Created mood: {mood.mood}')
        
        # Create demo challenge
        challenge, created = Challenge.objects.get_or_create(
            profile=profile,
            defaults={
                'challenge_type': 'daily_reflection',
                'stake': 20,
                'start_date': date.today() - timedelta(days=3),
                'end_date': date.today() + timedelta(days=4)
            }
        )
        
        if created:
            self.stdout.write('  Created demo challenge')
        
        # Create demo nudges
        nudge_messages = [
            {'nudge_type': 'time_reminder', 'message': 'Quick vibe check? 😊', 'tone': 'gen_z'},
            {'nudge_type': 'streak_motivation', 'message': 'Your streak is looking amazing! 🔥', 'tone': 'gen_z'},
        ]
        
        for nudge_info in nudge_messages:
            nudge, created = Nudge.objects.get_or_create(
                profile=profile,
                message=nudge_info['message'],
                defaults=nudge_info
            )
            if created:
                self.stdout.write(f'  Created nudge: {nudge.nudge_type}')
        
        # Create some coin transactions
        transaction_types = ['earn_mood', 'earn_reflection', 'earn_feedback']
        for i, trans_type in enumerate(transaction_types):
            CoinTransaction.objects.get_or_create(
                profile=profile,
                transaction_type=trans_type,
                defaults={
                    'amount': 1 if trans_type != 'earn_reflection' else 2,
                    'balance_after': profile.coin_balance,
                    'created_at': timezone.now() - timedelta(days=i)
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated demo data')
        )
        self.stdout.write(
            self.style.WARNING(
                'Demo user credentials: username=demo_user, password=demo123'
            )
        )
