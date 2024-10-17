from django.shortcuts import render, redirect
from .models import Mood
from .forms import MoodForm
from textblob import TextBlob
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# import csv
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
import pandas as pd
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from .forms import MoodForm



def home_view(request):
    if request.user.is_authenticated:
        # If the user is authenticated, redirect to the log mood page
        return redirect('log_mood')
    else:
        # If the user is not authenticated, render the home page
        return render(request, 'tracker/home.html')

def is_staff(user):
    return user.is_staff

def NotStaffView(request):
    return render(request, 'tracker/notstaff.html')

@user_passes_test(is_staff, login_url='notstaff')  # Redirect to notstaff if the user is not staff
def sentiment_analysis(request):
    # Use ORM aggregation to directly get average sentiments by user
    user_average_sentiments = (
        Mood.objects.filter(sentiment__isnull=False)
        .values('user__username')  # Group by user
        .annotate(average_sentiment=Avg('sentiment'))  # Calculate average
        .order_by('user__username')  # Optional ordering
    )
    
    # Convert QuerySet to a DataFrame for further analysis
    df = pd.DataFrame(user_average_sentiments)

    # Group by 'average_sentiment' and get counts for sentiment chart
    sentiment_counts = df['average_sentiment'].value_counts()

    # Prepare labels and values for the chart
    sentiment_labels = sentiment_counts.index.tolist()
    sentiment_values = sentiment_counts.values.tolist()

    return render(request, 'tracker/sentiment_analysis.html', {
        'user_average_sentiments': df.to_dict(orient='records'),
        'sentiment_labels': sentiment_labels,
        'sentiment_values': sentiment_values,
    })

def not_staff_view(request):
    return render(request, 'tracker/notstaff.html')  # Render notstaff.html

def user_login(request):
    print("Login view accessed")  # This should appear in the terminal
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Trying to log in user: {username}")  # Debug print
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print("User authenticated successfully")  # Debug print
            login(request, user)
            return redirect('log_mood')  # Redirect to the log mood page
        else:
            print("Authentication failed")  # Debug print
            return render(request, 'tracker/login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'tracker/login.html')


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user but do not commit yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()  # Save the user to the database

            messages.success(request, 'Registration successful! You can now log in.')
            auth_login(request, user)  # Log the user in
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()  # Instantiate a new form

    # Render the form with potential errors
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def log_mood(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)

        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user  # Set the user for the mood entry
            mood_entry.mood = mood_entry.mood.capitalize()  # Capitalize the mood

            # Debugging print statements
            print(f"Logging mood for user: {mood_entry.user.username}, Mood: {mood_entry.mood}, Notes: {mood_entry.notes}")

            # Perform sentiment analysis
            if mood_entry.notes:
                sentiment = TextBlob(mood_entry.notes).sentiment
                mood_entry.sentiment = sentiment.polarity if sentiment.polarity is not None else 0.0  # Fallback to neutral sentiment

            mood_entry.save()
            messages.success(request, f'Your mood "{mood_entry.mood}" has been recorded successfully!')
            return redirect('mood_history')
        else:
            print("Form is not valid:", form.errors)  # Print out any validation errors
            messages.error(request, "There was an error with your submission. Please check your input.")

            # Check if the form is empty
            if not request.POST.get('mood') or not request.POST.get('notes'):
                messages.error(request, "Please fill in all required fields.")
    else:
        form = MoodForm()

    return render(request, 'tracker/log_mood.html', {'form': form})





@login_required
def mood_history(request):
    moods = Mood.objects.filter(user=request.user).order_by('-created_at')  # Adjust field names as necessary

    # Prepare data for visualization
    mood_data = {
        "moods": [],
        "timestamps": [],
    }

    # Populate mood_data
    for mood in moods:
        mood_data["moods"].append(mood.mood)
        mood_data["timestamps"].append(mood.created_at)  # Ensure this field is populated

    # Create a DataFrame
    df = pd.DataFrame(mood_data)

    # Group by mood to get counts
    mood_counts = df['moods'].value_counts()

    # Prepare mood_labels and mood_values for the chart
    mood_labels = mood_counts.index.tolist()
    mood_values = mood_counts.values.tolist()

    # Define colors for each mood
    mood_colors = {
        "happy": "#6366f1",
        "neutral": "#6b7280",
        "sad": "#374151",
    }

    # Map colors to the labels
    colors = [mood_colors.get(mood, "#d1d5db") for mood in mood_labels]

    return render(request, 'tracker/mood_history.html', {
        'moods': moods,
        'mood_labels': mood_labels,
        'mood_values': mood_values,
        'colors': colors,
    })




# @login_required
# def export_csv(request):
#     moods = Mood.objects.filter(user=request.user)
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="moods.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Mood', 'Notes', 'Date'])
#     for mood in moods:
#         writer.writerow([mood.mood, mood.notes, mood.created_at])

#     return response

@login_required
def export_json(request):
    if request.method == 'POST':
        # Assuming username is sent in POST request for authentication
        username = request.POST.get('username')  # Use POST data
        password = request.POST.get('password')  # Assuming password is also sent

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('export_json')  # Redirect to the same page after login

        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    # If the request is not POST, return the moods as JSON
    moods = list(Mood.objects.filter(user=request.user).values())
    return JsonResponse({'moods': moods}, safe=False)  # Corrected JsonResponse
