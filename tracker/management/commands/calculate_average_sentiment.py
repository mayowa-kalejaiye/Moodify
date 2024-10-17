# tracker/management/commands/calculate_average_sentiment.py
from django.core.management.base import BaseCommand
from django.db.models import Avg, Case, When, IntegerField
from tracker.models import Mood  # Ensure the import is correct

class Command(BaseCommand):
    help = 'Calculate average sentiment for moods and overall average sentiment'

    def handle(self, *args, **kwargs):
        # Calculate average sentiment for each user
        moods_with_numeric_sentiment = (
            Mood.objects.annotate(
                sentiment_numeric=Case(
                    When(sentiment='happy', then=1),
                    When(sentiment='neutral', then=0),
                    When(sentiment='sad', then=-1),
                    default=None,
                    output_field=IntegerField(),
                )
            )
            .values('user__username')  # Group by username
            .annotate(average_sentiment=Avg('sentiment_numeric'))  # Calculate average sentiment
        )
        
        # Output the average sentiment for each user
        self.stdout.write("Average sentiment by user:")
        for mood in moods_with_numeric_sentiment:
            self.stdout.write(f"{mood['user__username']}: {mood['average_sentiment']}")  # Print formatted output

        # Calculate and output overall average sentiment
        overall_average_sentiment = (
            Mood.objects.annotate(
                sentiment_numeric=Case(
                    When(sentiment='happy', then=1),
                    When(sentiment='neutral', then=0),
                    When(sentiment='sad', then=-1),
                    default=None,
                    output_field=IntegerField(),
                )
            ).aggregate(Avg('sentiment_numeric'))['sentiment_numeric__avg']
        )
        self.stdout.write(f'Overall average sentiment: {overall_average_sentiment}')
