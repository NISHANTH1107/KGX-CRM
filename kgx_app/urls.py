from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home_redirect, name="home_redirect"),
   path('login', views.login_view, name="login"),
   path('logout/', views.logout_view, name='logout'),
   path('dashboard/', views.dashboard_view, name='dashboard'),
   path('profile/', views.profile, name='profile'),
   path('student/tasks/', views.student_tasks, name='student_tasks'),
   path('wifi/', views.wifi_view, name='wifi'),
   path('work_on_holidays/', views.work_on_holidays, name='work_on_holidays'),
   path('internship/', views.internship, name='internship'),
   path('contact/', views.contact_view, name='contact'),
   path('add_comment/', views.add_comment, name='add_comment'),
   path('inventory/', views.inventory, name='inventory'),
   path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
   path('assign-task/', views.assign_task, name='assign_task'),
    path('staff/to-do/', views.to_do_view, name='to_do'),
    path('staff/in-progress/', views.in_progress_view, name='in_progress'),
    path('staff/done/', views.done_view, name='done'),
    path('for_review/', views.for_review, name='for_review'),
    path('review-task/<int:task_id>/', views.review_task, name='review_task'),
    path('student/tasks/start/<int:task_id>/', views.start_task, name='start_task'),
    path('submit_task_link/<int:task_id>/', views.submit_task_link, name='submit_task_link'),]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)