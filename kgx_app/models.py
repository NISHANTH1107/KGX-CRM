from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(primary_key=True, max_length=20)
    dept = models.CharField(max_length=100)
    email_p = models.EmailField()
    email_clg = models.EmailField()
    phn_no = models.IntegerField()
    linked_in = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    domain = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    hackathon = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    
    def __str__(self):
        return self.roll_no


class Wifi(models.Model):
    roll_no = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mac = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.roll_no} - {self.mac}"



from django.db import models
from django.core.exceptions import ValidationError

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



class Hackathon(models.Model):
    image = models.ImageField(upload_to='images/')
    link = models.URLField()

    def __str__(self):
        return self.image.name
    
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