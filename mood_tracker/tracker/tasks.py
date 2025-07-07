"""
Celery tasks for the MoodSync Behavior Engine
"""
from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def streak_evaluator_task():
    """
    Daily task to evaluate streaks and apply penalties for inactivity
    Runs daily at 01:00 via Celery Beat
    """
    from .models import Profile, CoinTransaction
    
    logger.info("Starting streak evaluator task")
    
    today = date.today()
    three_days_ago = today - timedelta(days=3)
    
    # Get all profiles
    profiles = Profile.objects.all()
    
    for profile in profiles:
        try:
            # Update streak for each user
            profile.update_streak()
            
            # Check for inactivity penalty (no mood log for 3+ days)
            if (profile.last_mood_log and 
                profile.last_mood_log <= three_days_ago and 
                profile.coin_balance > 0):
                
                # Apply penalty
                profile.coin_balance = max(0, profile.coin_balance - 1)
                profile.save()
                
                # Create transaction record
                CoinTransaction.objects.create(
                    profile=profile,
                    transaction_type='lose_inactive',
                    amount=-1,
                    balance_after=profile.coin_balance
                )
                
                logger.info(f"Applied inactivity penalty to user {profile.user.username}")
                
        except Exception as e:
            logger.error(f"Error processing profile {profile.user.username}: {e}")
    
    logger.info("Streak evaluator task completed")

@shared_task
def challenge_settler_task():
    """
    Hourly task to settle completed challenges
    Runs hourly via Celery Beat
    """
    from .models import Challenge, CoinTransaction
    
    logger.info("Starting challenge settler task")
    
    today = date.today()
    
    # Get challenges that have ended but not been settled
    challenges = Challenge.objects.filter(
        end_date__lt=today,
        settled=False
    )
    
    for challenge in challenges:
        try:
            # Check if challenge was completed
            challenge.check_completion()
            
            if challenge.completed:
                # User won - double the stake
                reward = challenge.stake * 2
                challenge.profile.coin_balance += reward
                challenge.profile.save()
                
                # Create transaction record
                CoinTransaction.objects.create(
                    profile=challenge.profile,
                    transaction_type='win_challenge',
                    amount=reward,
                    balance_after=challenge.profile.coin_balance,
                    challenge=challenge
                )
                
                logger.info(f"User {challenge.profile.user.username} won challenge, rewarded {reward} coins")
                
            else:
                # User lost - coins already deducted when challenge was created
                # Create transaction record for the loss
                CoinTransaction.objects.create(
                    profile=challenge.profile,
                    transaction_type='lose_challenge',
                    amount=0,  # No additional loss, just record keeping
                    balance_after=challenge.profile.coin_balance,
                    challenge=challenge
                )
                
                logger.info(f"User {challenge.profile.user.username} lost challenge")
            
            # Mark challenge as settled
            challenge.settled = True
            challenge.save()
            
        except Exception as e:
            logger.error(f"Error settling challenge {challenge.id}: {e}")
    
    logger.info("Challenge settler task completed")

@shared_task
def generate_contextual_nudges_task():
    """
    Task to generate contextual nudges for users
    Can be run periodically or triggered by events
    """
    from .models import Profile, Nudge, Mood
    
    logger.info("Starting contextual nudges generation task")
    
    today = date.today()
    profiles = Profile.objects.all()
    
    for profile in profiles:
        try:
            # Limit to 3 nudges per day
            daily_nudges = Nudge.objects.filter(
                profile=profile,
                created_at__date=today
            ).count()
            
            if daily_nudges >= 3:
                continue
                
            # Check if user needs a nudge
            has_mood_today = Mood.objects.filter(
                user=profile.user,
                created_at__date=today
            ).exists()
            
            if not has_mood_today:
                # Check if user already has unviewed nudges
                unviewed_nudges = Nudge.objects.filter(
                    profile=profile,
                    viewed=False
                ).count()
                
                if unviewed_nudges == 0:
                    # Generate a new nudge
                    nudge = _generate_nudge_for_profile(profile)
                    if nudge:
                        logger.info(f"Generated nudge for user {profile.user.username}")
                        
        except Exception as e:
            logger.error(f"Error generating nudges for profile {profile.user.username}: {e}")
    
    logger.info("Contextual nudges generation task completed")

def _generate_nudge_for_profile(profile):
    """Helper function to generate a nudge for a specific profile"""
    from .models import Nudge, Mood
    from datetime import date, timedelta
    import random
    
    today = date.today()
    
    # Determine tone based on age
    tone = 'gen_z' if profile.age and profile.age < 30 else 'professional'
    
    # Check recent mood pattern
    recent_moods = Mood.objects.filter(
        user=profile.user,
        created_at__date__gte=today - timedelta(days=3)
    ).order_by('-created_at')
    
    if recent_moods.exists():
        avg_rating = sum(m.rating for m in recent_moods) / len(recent_moods)
        if avg_rating < 3:
            # Negative trend - supportive message
            nudge_type = 'mood_trend'
            message = _get_support_message(tone, profile.streak_count)
        else:
            # General reminder
            nudge_type = 'time_reminder'
            message = _get_reminder_message(tone, profile.streak_count)
    else:
        # No recent moods - skip pattern alert
        nudge_type = 'skip_pattern'
        message = _get_skip_message(tone, profile.streak_count)
    
    # Create nudge
    nudge = Nudge.objects.create(
        profile=profile,
        nudge_type=nudge_type,
        message=message,
        tone=tone
    )
    
    return nudge

def _get_support_message(tone, streak_count):
    """Get supportive message for negative mood trends"""
    if tone == 'gen_z':
        messages = [
            "Hey, sounds like you're going through it rn. Take a sec to check in with yourself? 💙",
            "Tough vibes lately? Your feelings are valid - maybe log how you're doing? 🫂",
            "Not feeling it today? That's totally okay. Quick mood check-in? ✨"
        ]
    else:
        messages = [
            "It seems like you've been experiencing some challenges lately. Consider taking a moment to reflect on your current state.",
            "Your recent mood patterns suggest you might benefit from some self-reflection. How are you feeling today?",
            "Taking time to acknowledge your emotions can be helpful. Would you like to log your current mood?"
        ]
    
    import random
    return random.choice(messages)

def _get_reminder_message(tone, streak_count):
    """Get reminder message for mood logging"""
    if tone == 'gen_z':
        messages = [
            f"Your {streak_count}-day streak is looking fire! 🔥 Keep it going?",
            "Quick vibe check? How are you feeling today? 😊",
            "Your mood matters! Drop a quick check-in? 💭"
        ]
    else:
        messages = [
            f"You've maintained a {streak_count}-day reflection streak. Continue with today's mood log?",
            "Regular mood tracking helps build self-awareness. How are you feeling today?",
            "Taking a moment to reflect on your current emotional state can be beneficial."
        ]
    
    import random
    return random.choice(messages)

def _get_skip_message(tone, streak_count):
    """Get message for users who haven't logged recently"""
    if tone == 'gen_z':
        messages = [
            "Miss us? 👀 How have you been feeling lately?",
            "Been a while! Quick check-in? Your mental health matters 💚",
            "Hey stranger! Ready to get back on track? 🌟"
        ]
    else:
        messages = [
            "It's been a while since your last mood log. How are you feeling today?",
            "Regular check-ins can help maintain emotional awareness. Would you like to log your current mood?",
            "Consistent reflection is beneficial for emotional well-being. How are you today?"
        ]
    
    import random
    return random.choice(messages)
