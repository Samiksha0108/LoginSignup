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
        exclude = ['user']

# class JobRoleForm(forms.ModelForm):
#     class Meta:
#         model = JobRole
#         exclude = ['user']
from django import forms
from .models import JobRole
from .utils import extract_keywords

class JobRoleForm(forms.ModelForm):
    selected_keywords = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label="Mandatory Keywords"
    )

    class Meta:
        model = JobRole
        exclude = ['user', 'keywords']

    


