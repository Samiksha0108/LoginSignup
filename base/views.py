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

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})



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

