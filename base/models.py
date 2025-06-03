from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.user.username


#new
from django.db import models
from django.contrib.auth.models import User

SALARY_TYPE_CHOICES = [
    ('hr', 'Hr'),
    ('yr', 'Yr'),
]

EMPLOYMENT_TYPE_CHOICES = [
    ('full-time', 'Full-time'),
    ('part-time', 'Part-time'),
    ('contract', 'Contract'),
]

EXPERIENCE_LEVEL_CHOICES = [
    ('entry', 'Entry'),
    ('mid', 'Mid'),
    ('senior', 'Senior'),
]

from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Company who added
    linked_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')  # Candidate user

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    role = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    govt_id_number = models.CharField(max_length=100)
    ssn_number = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


# class JobRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Company who posted
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     salary_min = models.DecimalField(max_digits=10, decimal_places=2)
#     salary_max = models.DecimalField(max_digits=10, decimal_places=2)
#     employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES)
#     location = models.CharField(max_length=100)
#     experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES)

#     def __str__(self):
#         return self.title


class JobRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=15, choices=[
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract')
    ])
    location = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=10, choices=[
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior')
    ])
    keywords = models.TextField(blank=True)


    def get_keyword_list(self):
        return self.keywords.split(",") if self.keywords else []


# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Timesheet(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def hours_worked(self):
        return round((self.end_time - self.start_time).total_seconds() / 3600, 2)

    def __str__(self):
        return f"{self.employee} | {self.start_time} to {self.end_time} | Approved: {self.approved}"
