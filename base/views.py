from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
#from .models import Profile
#from django.contrib.auth import views as auth_views


@login_required
def home(request):
 return render(request, "home.html", {})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


# def authView(request):
#  if request.method == "POST":
#   form = UserCreationForm(request.POST or None)
#   if form.is_valid():
#    form.save()
#    return redirect("base:login")
#  else:
#   form = UserCreationForm()
#  return render(request, "registration/signup.html", {"form": form})
# from .forms import CustomUserCreationForm
# from .models import Profile

# from .forms import CustomUserCreationForm
# from .models import Profile

# def authView(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             resume_file = form.cleaned_data.get('resume')
#             Profile.objects.create(user=user, resume=resume_file)
#             return redirect("login")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "registration/signup.html", {"form": form})

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Profile

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

