from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view,match_resume_view,job_match_all_resumes_view
app_name = 'base'


urlpatterns = [
    path('', views.profile, name='profile'),
    # In base/urls.py
    path('', views.profile, name='home'),  # ✅ now matches LOGIN_REDIRECT_URL

    path('signup/', views.authView, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('match-resume/', match_resume_view, name='match_resume'),
    path('match-job-to-resumes/', job_match_all_resumes_view, name='match_job_all'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.user_job_postings, name='my_jobs'),
    path('my-employees/', views.view_employees, name='view_employees'),
    path('employee/info/', views.employee_info, name='employee_info'),
    path('submit-timesheet/', views.submit_timesheet, name='submit_timesheet'),
    path('view-timesheets/', views.view_timesheets, name='view_timesheets'),
    path('approve-timesheet/<int:timesheet_id>/', views.approve_timesheet, name='approve_timesheet'),
    path('employee/timesheets/', views.view_employee_timesheets, name='view_employee_timesheets'),
    path('timesheet/approve/<int:timesheet_id>/', views.approve_timesheet, name='approve_timesheet'),
    path('timesheet/reject/<int:timesheet_id>/', views.reject_timesheet, name='reject_timesheet'),





]


