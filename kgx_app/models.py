from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

class Profile(models.Model):
    STUDENT = 'student'
    STAFF = 'staff'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (STAFF, 'Staff'),
    ]
    
    
    name = models.CharField(max_length=100)
    roll_no = models.CharField(primary_key=True, max_length=20)
    dept = models.CharField(max_length=100)
    email_p = models.EmailField()
    email_clg = models.EmailField()
    phn_no = models.CharField(max_length=15)
    linked_in = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    domain = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    hackathon = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return self.roll_no

class Wifi(models.Model):
    roll_no = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=50)
    screenshot = models.ImageField(upload_to='wifi_screenshots/' , null=True, blank=True)  # Upload directory for screenshots
    submitted_at = models.DateTimeField(auto_now_add=True , null=True, blank=True)

    def __str__(self):
        return f"{self.roll_no} - {self.mac_address}"

class Holiday(models.Model):
    name = models.CharField(max_length=100, verbose_name="Holiday Name")
    department = models.CharField(max_length=100, verbose_name="Department")
    purpose = models.CharField(max_length=200, verbose_name="Purpose of Holiday")
    entry_time = models.TimeField(verbose_name="Entry Time")
    exit_time = models.TimeField(verbose_name="Exit Time")
    date_submitted = models.DateTimeField(default=timezone.now)


    def clean(self):
        # Custom validation to ensure exit_time is after entry_time
        if self.exit_time <= self.entry_time:
            raise ValidationError('Exit time must be after entry time.')

    def __str__(self):
        return f"{self.name} ({self.department}) - {self.entry_time}"


class Internship(models.Model):
    image = models.ImageField(upload_to='images/')
    link = models.URLField()

    def __str__(self):
        return self.image.name
    

class Learnbypractice(models.Model):
    image = models.ImageField(upload_to='images/')
    link = models.URLField()

    def __str__(self):
        return self.image.name
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."  # Show first 20 characters
    
    def is_recent(self):
        return (timezone.now() - self.created_at) <= timezone.timedelta(hours=24)
    



class ToDo(models.Model):
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    reference_link = models.URLField(blank=True, null=True)
    due_date = models.DateField()

    def __str__(self):
        return self.task_title

class InProgress(models.Model):
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    reference_link = models.URLField(blank=True, null=True)
    due_date = models.DateField()

    def __str__(self):
        return self.task_title
    

class ForReview(models.Model):
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    reference_link = models.URLField(blank=True, null=True)
    task_link = models.URLField()  # New field for the submitted link
    due_date = models.DateField()

    def __str__(self):
        return self.task_title
    
class Done(models.Model):
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    reference_link = models.URLField(blank=True, null=True)
    due_date = models.DateField()
    task_link = models.URLField(blank=True, null=True)  # Include task link field

    def __str__(self):
        return self.task_title