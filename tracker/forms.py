from django import forms
from .models import Mood
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import bleach

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood', 'notes']  # Ensure you include the correct fields from your model

        def clean_notes(self):
            notes = self.cleaned_data.get('notes')
            # Sanitize the input to prevent XSS
            return bleach.clean(notes)
        
        def sanitize_input(self, input_text):
            # Escape HTML to prevent XSS
            return input_text.replace('<', '&lt;').replace('>', '&gt;')

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email or '.' not in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        if len(password1) <= 6:
            raise forms.ValidationError("Password must be at least 7 characters long.")

        # Check if the username already exists
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")

        # Check if the email already exists
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists. Please choose a different one.")

        # Call the clean_email method to validate the email format
        self.clean_email()
