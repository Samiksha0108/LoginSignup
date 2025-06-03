from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# views.py
from .models import Profile, User
from .utils import extract_text, match_resume_to_job
from .forms import JobToResumesForm




@login_required
def home(request):
 return render(request, "home.html", {})

from django.contrib.auth.decorators import login_required

# @login_required
# def profile(request):
#     profile = request.user.profile
#     return render(request, 'profile.html', {'profile': profile})
#new
from .models import JobRole

# @login_required
# def profile(request):
#     profile = request.user.profile
#     job_roles = JobRole.objects.filter(user=request.user)
#     return render(request, 'profile.html', {
#         'profile': profile,
#         'job_roles': job_roles
#     })
# from .models import JobRole

# @login_required
# def profile(request):
#     profile = request.user.profile
#     job_posts = JobRole.objects.filter(user=request.user).order_by('-id')
#     return render(request, 'profile.html', {
#         'profile': profile,
#         'job_posts': job_posts
#     })

from .models import JobRole, Employee

@login_required
def profile(request):
    profile = request.user.profile
    job_posts = JobRole.objects.filter(user=request.user).order_by('-id')
    employees = Employee.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'profile': profile,
        'job_posts': job_posts,
        'employees': employees,
    })



# views.py

from django.contrib.auth import login
from .models import Employee

def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            resume = form.cleaned_data.get('resume')

            # Create profile
            profile, created = Profile.objects.get_or_create(user=user)
            if resume:
                profile.resume = resume
                profile.save()

            # 🔗 Try to match to any pre-added Employee by email
            employee_qs = Employee.objects.filter(email=user.username, linked_user__isnull=True)
            if employee_qs.exists():
                employee = employee_qs.first()
                employee.linked_user = user
                employee.save()
                print(f"Linked employee {employee} to signed-up user {user}")

            return redirect('base:login')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# def authView(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             resume = form.cleaned_data.get('resume')

#             # Either get existing profile or create it
#             profile, created = Profile.objects.get_or_create(user=user)
#             if resume:
#                 profile.resume = resume
#                 profile.save()

#             # After user = form.save()
#             from .models import Employee
#             try:
#                 employee = Employee.objects.get(email=user.email)
#                 employee.linked_user = user
#                 employee.save()
#             except Employee.DoesNotExist:
#                 pass


#             return redirect('base:login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "registration/signup.html", {"form": form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('base:login')

from .forms import ResumeMatchForm
from .utils import extract_text, match_resume_to_job,extract_keywords
from django.contrib.auth.decorators import login_required

@login_required
def match_resume_view(request):
    result = None
    if request.method == "POST":
        form = ResumeMatchForm(request.POST)
        if form.is_valid():
            job_desc = form.cleaned_data['job_description']
            profile = request.user.profile

            if profile.resume:
                resume_path = profile.resume.path
                resume_text = extract_text(resume_path)
                score, matched = match_resume_to_job(resume_text, job_desc)

                result = {
                    'score': score,
                    'matched': matched,
                }
            else:
                result = {'error': 'No resume found in your profile. Please upload one first.'}
    else:
        form = ResumeMatchForm()

    return render(request, 'match_resume.html', {'form': form, 'result': result})





@login_required
def job_match_all_resumes_view(request):
    results = []
    job_kw = None

    if request.method == "POST":
        form = JobToResumesForm(request.POST)
        if form.is_valid():
            job_desc = form.cleaned_data['job_description']
            job_kw = extract_keywords(job_desc)

            for profile in Profile.objects.exclude(resume=''):
                try:
                    resume_path = profile.resume.path
                    resume_text = extract_text(resume_path)
                    score, matched = match_resume_to_job(resume_text, job_desc)

                    results.append({
                        'user': profile.user.username,
                        'score': score,
                        'matched_keywords': matched
                    })
                except Exception as e:
                    print(f"Error processing {profile.user.username}: {e}")
                    continue

            results.sort(key=lambda x: x['score'], reverse=True)
    else:
        form = JobToResumesForm()

    return render(request, 'job_to_resumes.html', {
        'form': form,
        'results': results,
        'job_keywords': sorted(job_kw) if job_kw else None
    })


#new
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm, JobRoleForm
from .models import Employee, JobRole

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('base:dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

# @login_required
# def post_job(request):
#     if request.method == 'POST':
#         form = JobRoleForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.user = request.user
#             job.save()
#             return redirect('base:dashboard')
#     else:
#         form = JobRoleForm()
#     return render(request, '/Users/samiksha/LoginandSignup/User-Authentication-and-User-Signup-in-Python-using-Django-/loginSignup/base/templates/post_job.html', {'form': form})


# @login_required
# def post_job(request):
#     description = None
#     keywords_choices = []

#     if request.method == 'POST':
#         description = request.POST.get('description')
#         if description:
#             keywords_choices = extract_keywords(description)

#         form = JobRoleForm(request.POST)
#         # ✅ Repopulate choices BEFORE validation
#         form.fields['selected_keywords'].choices = [(kw, kw) for kw in sorted(keywords_choices)]

#         if 'preview_keywords' in request.POST:
#             # Preview mode: just show extracted checkboxes
#             pass
#         else:
#             # Final submit: validate and save
#             if form.is_valid():
#                 job = form.save(commit=False)
#                 job.user = request.user
#                 keywords = form.cleaned_data.get('selected_keywords', [])

#                 print("Extracted keywords list:", keywords)  # Should print a list
#                 joined_keywords = ",".join([str(k) for k in keywords])
#                 print("Joined keyword string:", joined_keywords)  # Should print "Git,Python" etc.

#                 job.keywords = (keywords)
#                 print(job.keywords)
#                 job.save()

#                 return redirect('base:dashboard')

#     else:
#         form = JobRoleForm()

#     return render(request, 'post_job.html', {'form': form})

@login_required
def post_job(request):
    description = None
    keywords_choices = []

    if request.method == 'POST':
        description = request.POST.get('description')

        if description:
            keywords_choices = extract_keywords(description)
            print("Extracted keywords:", keywords_choices)  # Debug log

        # Always build the form with POST data
        form = JobRoleForm(request.POST)
        # ✅ Always update keyword choices before validating
        form.fields['selected_keywords'].choices = [(kw, kw) for kw in sorted(keywords_choices)]

        if 'preview_keywords' in request.POST:
            # Just redisplay form with checkboxes populated
            return render(request, 'post_job.html', {'form': form})
        else:
            # Submit final form
            if form.is_valid():
                job = form.save(commit=False)
                job.user = request.user

                # Get selected checkbox keywords
                keywords = form.cleaned_data.get('selected_keywords', [])
                if isinstance(keywords, str):
                    keywords = [keywords]

                # Get manually entered keywords
                manual_kw = form.cleaned_data.get('manual_keywords', '')
                manual_kw_list = [kw.strip() for kw in manual_kw.split(',') if kw.strip()]

                # Combine both
                all_keywords = keywords + manual_kw_list

                job.keywords = ",".join(all_keywords)
                job.save()
                return redirect('base:dashboard')

            else:
                print("Form errors:", form.errors)  # Debug
    else:
        form = JobRoleForm()

    return render(request, 'post_job.html', {'form': form})

from .models import JobRole

@login_required
def user_job_postings(request):
    user_jobs = JobRole.objects.filter(user=request.user)
    return render(request, 'user_job_postings.html', {'jobs': user_jobs})

@login_required
def view_employees(request):
    employees = Employee.objects.filter(user=request.user)
    return render(request, 'view_employees.html', {'employees': employees})

@login_required
def employee_info(request):
    try:
        emp = request.user.employee_profile  # via related_name
        print(emp)
        print("---")
    except Employee.DoesNotExist:
        print(" [][][][]")
        emp = None

    return render(request, 'employee_info.html', {'employee': emp})


# views.py
from .models import Timesheet, Employee
from .forms import TimesheetForm
from django.contrib.auth.decorators import login_required

@login_required
def submit_timesheet(request):
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            try:
                timesheet.employee = Employee.objects.get(linked_user=request.user)
                timesheet.save()
                return redirect('base:view_timesheets')
            except Employee.DoesNotExist:
                return render(request, 'error.html', {'message': "You're not a registered employee."})
    else:
        form = TimesheetForm()
    return render(request, 'submit_timesheet.html', {'form': form})


from django.utils import timezone
from datetime import timedelta
from django.db import models  # ✅ Add this if not already present


@login_required
def view_timesheets(request):
    if Employee.objects.filter(user=request.user).exists():
        # Company user: show only pending timesheets of employees they added
        added_employees = Employee.objects.filter(user=request.user)
        timesheets = Timesheet.objects.filter(
            employee__in=added_employees,
            approved=False,
            rejected=False
        ).order_by('-start_time')
        is_company = True
    else:
        # Employee user: show all their timesheets (approved, rejected, pending)
        try:
            employee = Employee.objects.get(linked_user=request.user)
            timesheets = Timesheet.objects.filter(employee=employee).order_by('-start_time')
            is_company = False
        except Employee.DoesNotExist:
            timesheets = []
            is_company = False

    return render(request, 'view_timesheets.html', {
        'timesheets': timesheets,
        'is_company': is_company
    })



@login_required
def approve_timesheet(request, timesheet_id):
    timesheet = Timesheet.objects.get(id=timesheet_id)
    if timesheet.employee.user == request.user:  # Only company who added the employee
        timesheet.approved = True
        timesheet.save()
    return redirect('base:view_timesheets')

@login_required
def reject_timesheet(request, timesheet_id):
    timesheet = Timesheet.objects.get(id=timesheet_id)
    if timesheet.employee.user == request.user:
        timesheet.rejected = True
        timesheet.save()
    return redirect('base:view_timesheets')


@login_required
def view_employee_timesheets(request):
    try:
        employee = Employee.objects.get(linked_user=request.user)
        approved_timesheets = Timesheet.objects.filter(employee=employee, approved=True)
        pending_timesheets = Timesheet.objects.filter(employee=employee, approved=False, rejected=False)
        rejected_timesheets = Timesheet.objects.filter(employee=employee, approved=False, rejected=True)
    except Employee.DoesNotExist:
        approved_timesheets = []
        pending_timesheets = []

    return render(request, 'view_employee_timesheets.html', {
        'timesheets': approved_timesheets,
        'timesheets1': pending_timesheets,
        'timesheets2': rejected_timesheets
    })
