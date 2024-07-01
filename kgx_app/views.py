from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Profile,Hackathon,Learnbypractice,Internship

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')  # Redirect to a home page or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def dashboard_view(request):
    return render(request, 'dashboard.html')

def profile(request):
    profile = get_object_or_404(Profile, roll_no=request.user.username)
    return render(request, 'profile.html', {'profile': profile})
    

def learn_by_practice(request):
    learnbypractices = Learnbypractice.objects.all()
    return render(request, 'learnbypractice.html', {'learnbypractices': learnbypractices})

def wifi(request):
    return render(request, 'wifi.html')

def work_on_holidays(request):
    return render(request, 'work_on_holidays.html')

def hackathon(request):
    images = Hackathon.objects.all()
    return render(request, 'hackathon.html', {'images': images})

def internship(request):
    internships = Internship.objects.all()
    return render(request, 'internship.html', {'internships': internships})

def inventory(request):
    return render(request, 'inventory.html')