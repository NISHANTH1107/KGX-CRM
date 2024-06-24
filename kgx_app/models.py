from django.db import models
from django.contrib.auth.models import User



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
    
    def __str__(self):
        return self.roll_no


class Wifi(models.Model):
    roll_no = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mac = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.roll_no} - {self.mac}"


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.ForeignKey(Profile, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    date = models.DateField()
    
    def __str__(self):
        return f"{self.name} ({self.roll_no}) - {self.date}"
