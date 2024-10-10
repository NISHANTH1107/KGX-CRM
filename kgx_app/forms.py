from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Holiday
from .models import Comment
from .models import Wifi

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

class WifiForm(forms.ModelForm):
    roll_no = forms.CharField(max_length=100, required=True)  
    mac_address = forms.CharField(max_length=100, required=True)
    screenshot = forms.ImageField(required=True)

    class Meta:
        model = Wifi  
        fields = ['roll_no', 'mac_address', 'screenshot']
