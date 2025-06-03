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

#new
from django import forms
from .models import Employee, JobRole

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user','linked_user']  # Exclude user and linked_user fields

# class JobRoleForm(forms.ModelForm):
#     class Meta:
#         model = JobRole
#         exclude = ['user']
from django import forms
from .models import JobRole
from .utils import extract_keywords

from django import forms

class JobRoleForm(forms.ModelForm):
    selected_keywords = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select Extracted Keywords"
    )
    manual_keywords = forms.CharField(
        required=False,
        label="Add Your Own Keywords (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Leadership, Communication'})
    )

    class Meta:
        model = JobRole
        fields = ['title', 'description', 'salary_min', 'salary_max', 'employment_type', 'location', 'experience_level']


    


# forms.py
from django import forms
from .models import Timesheet

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
