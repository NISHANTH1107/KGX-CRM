from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input_user',
        'placeholder': 'Username...'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input_pass',
        'placeholder': 'Password...'
    }))

from django import forms
from .models import Holiday


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'department', 'purpose', 'entry_time', 'exit_time']
        widgets = {
            'entry_time': forms.TimeInput(attrs={'type': 'time'}),
            'exit_time': forms.TimeInput(attrs={'type': 'time'}),
        }