@echo off
echo Running Mood Tracker API tests...
python manage.py test mood_tracker.tracker --verbosity=2
echo.
echo Test run complete!
pause
