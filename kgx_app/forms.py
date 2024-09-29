from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Holiday
from .models import Comment

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input_user',
        'placeholder': 'Username...'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input_pass',
        'placeholder': 'Password...'
    }))

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'department', 'purpose', 'entry_time', 'exit_time']
        widgets = {
            'entry_time': forms.TimeInput(attrs={'type': 'time'}),
            'exit_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']