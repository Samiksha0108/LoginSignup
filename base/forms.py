from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    resume = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'resume']
class ResumeMatchForm(forms.Form):
    job_description = forms.CharField(widget=forms.Textarea, label="Paste Job Description")


# forms.py
class JobToResumesForm(forms.Form):
    job_description = forms.CharField(widget=forms.Textarea, label="Paste Job Description")

