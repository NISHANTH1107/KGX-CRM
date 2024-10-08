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
   path('learn_by_practice/', views.learn_by_practice, name='learn_by_practice'),
   path('wifi/', views.wifi, name='wifi'),
   path('work_on_holidays/', views.work_on_holidays, name='work_on_holidays'),
   path('internship/', views.internship, name='internship'),
   path('contact/', views.contact_view, name='contact'),
   path('add_comment/', views.add_comment, name='add_comment'),
   path('inventory/', views.inventory, name='inventory'),
   path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
   path('assign-task/', views.assign_task, name='assign_task'),
    path('to-do/', views.to_do, name='to_do'),
    path('in-progress/', views.in_progress, name='in_progress'),
    path('for-review/', views.for_review, name='for_review'),
    path('done/', views.done, name='done'),]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)