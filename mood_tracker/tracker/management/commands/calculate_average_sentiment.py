# tracker/management/commands/calculate_average_sentiment.py
from django.core.management.base import BaseCommand
from django.db.models import Avg, Case, When, IntegerField
from tracker.models import Mood 

class Command(BaseCommand):
    help = 'Calculate average sentiment for moods and overall average sentiment'

    def handle(self, *args, **kwargs):
        # Calculate average sentiment for each user
        # Using the actual sentiment field which is numeric in your API
        moods_by_user = (
            Mood.objects.filter(sentiment__isnull=False)  # Filter out null sentiments
            .values('user__username')  # Group by username
            .annotate(average_sentiment=Avg('sentiment'))  # Calculate average sentiment
            .order_by('-average_sentiment')  # Order by sentiment (highest first)
        )
        
        # Output the average sentiment for each user
        self.stdout.write(self.style.SUCCESS("Average sentiment by user:"))
        if not moods_by_user:
            self.stdout.write(self.style.WARNING("No mood data with sentiment found."))
        
        for mood in moods_by_user:
            sentiment_value = round(mood['average_sentiment'], 3) if mood['average_sentiment'] is not None else 'No data'
            sentiment_category = self._categorize_sentiment(mood['average_sentiment'])
            self.stdout.write(f"{mood['user__username']}: {sentiment_value} ({sentiment_category})")

        # Calculate and output overall average sentiment
        overall_result = Mood.objects.filter(sentiment__isnull=False).aggregate(Avg('sentiment'))
        overall_avg = overall_result['sentiment__avg']
        
        if overall_avg is not None:
            overall_category = self._categorize_sentiment(overall_avg)
            self.stdout.write(self.style.SUCCESS(f'Overall average sentiment: {round(overall_avg, 3)} ({overall_category})'))
        else:
            self.stdout.write(self.style.WARNING('No sentiment data available.'))
    
    def _categorize_sentiment(self, sentiment_value):
        """Categorize numeric sentiment values"""
        if sentiment_value is None:
            return "Unknown"
        elif sentiment_value > 0.5:
            return "Very Positive"
        elif sentiment_value > 0.1:
            return "Positive"
        elif sentiment_value > -0.1:
            return "Neutral"
        elif sentiment_value > -0.5:
            return "Negative"
        else:
            return "Very Negative"
