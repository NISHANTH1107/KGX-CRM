from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
   path('', views.login_view, name="login"),
   path('dashboard/', views.dashboard_view, name='home'),
   path('profile/', views.profile, name='profile'),
   path('learn_by_practice/', views.learn_by_practice, name='learn_by_practice'),
   path('wifi/', views.wifi, name='wifi'),
   path('work_on_holidays/', views.work_on_holidays, name='work_on_holidays'),
   path('hackathon/', views.hackathon, name='hackathon'),
   path('internship/', views.internship, name='internship'),
   path('inventory/', views.inventory, name='inventory')]