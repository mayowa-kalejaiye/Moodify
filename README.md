# Mood Tracker Application

This is a Django-based mood tracking web application. It allows users to log their moods, view mood history, perform sentiment analysis, and export their data in JSON format. The app also includes user authentication, allowing users to register, log in, and manage their moods.

## Features

- **User Authentication**: Users can register, log in, and log out using Django’s built-in authentication system.
- **Log Mood**: Users can log their mood along with additional notes. The sentiment analysis feature automatically analyzes the mood notes.
- **View Mood History**: Users can view their previously logged moods and visualize their mood history through charts.
- **Sentiment Analysis**: Admin users can view average sentiment analysis for all users.
- **Export Mood Data**: Users can export their mood history in JSON format.
- **Admin Panel**: Includes a staff-only view to access sentiment analysis and user statistics.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/yourusername/mood_tracker.git
cd mood_tracker
```

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies

Install the required dependencies listed in requirements.txt:

```bash
pip install -r requirements.txt
```

If requirements.txt is not present, install the required libraries manually

```bash
pip install django pandas textblob

```

### 4. Apply Migrations

Run the following command to apply the database migrations:

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)

To access the admin panel and perform sentiment analysis, create a superuser:

```bash
python manage.py createsuperuser
```

Now you can access the app at `http://127.0.0.1:8000/`.


### URL Endpoints

Here’s a breakdown of the URL endpoints for the app:

- `/log/`: Log your mood and notes.
- `/login/`: User login page.
- `/history/`: View your mood history with visualizations.
- `/export_json/`: Export your mood data as a JSON file.
- `/staff/`: (Admin Only) Perform sentiment analysis and view user mood statistics.
- `/admin/`: Django Admin panel.

### File Structure

The project structure is organized as follows:
```bash
mood_tracker/
│
├── mood_tracker/  # Django project folder
│   ├── settings.py  # Django settings
│   ├── urls.py  # Project URL configuration
│   ├── ...
│
├── tracker/  # Django app folder
│   ├── models.py  # Mood model
│   ├── views.py  # Views for logging moods, history, etc.
│   ├── urls.py  # App-specific URL configuration
│   ├── forms.py  # Forms for mood logging
│   ├── templates/  # HTML templates
│   ├── ...
│
├── venv/  # Virtual environment
│
└── manage.py  # Django management script
```

### Mood Model

The core model of the application is the Mood model, which contains the following fields:

- `mood`: A string indicating the user's mood (e.g., "happy", "sad", etc.).
- `notes`: Additional notes for the mood entry.
- `sentiment`: The sentiment score calculated using TextBlob.
- `created_at`: Timestamp for when the mood was logged.

### Sentiment Analysis

The sentiment analysis feature uses the TextBlob library to analyze mood notes. The sentiment score ranges from -1.0 (negative sentiment) to 1.0 (positive sentiment).

Admin users can view the average sentiment of all users through the `/staff/` URL.

### Exporting Data

Users can export their mood history in JSON format by clicking the Export json link in `/mood_history/`. This exports all mood data for the authenticated user.

### Visualizations

The mood history page visualizes mood data using charts. It breaks down moods by their frequency and shows them in different colors

### I don't know why I have it has to be an Open source project, but it's good...right?🫠
