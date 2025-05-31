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
from .models import JobRole

@login_required
def profile(request):
    profile = request.user.profile
    job_posts = JobRole.objects.filter(user=request.user).order_by('-id')
    return render(request, 'profile.html', {
        'profile': profile,
        'job_posts': job_posts
    })




def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            resume = form.cleaned_data.get('resume')

            # Either get existing profile or create it
            profile, created = Profile.objects.get_or_create(user=user)
            if resume:
                profile.resume = resume
                profile.save()

            return redirect('base:login')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
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
                keywords = form.cleaned_data.get('selected_keywords', [])
                if isinstance(keywords, str):
                    keywords = [keywords]
                job.keywords = ",".join(keywords)
                job.save()
                return redirect('base:dashboard')  # or 'base:dashboard'
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
