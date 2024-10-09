from django.contrib import admin
from django.contrib import admin
from .models import Profile, Wifi, Holiday,Internship,Learnbypractice,Comment

admin.site.register(Profile)
admin.site.register(Holiday)
admin.site.register(Internship)
admin.site.register(Learnbypractice)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')  # Add any fields you want to display
# Register your models here.

@admin.register(Wifi)
class WifiAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'mac_address', 'screenshot', 'submitted_at')