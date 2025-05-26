from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.profile, name='profile'),
    # In base/urls.py
    path('', views.profile, name='home'),  # ✅ now matches LOGIN_REDIRECT_URL

    path('signup/', views.authView, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

]
