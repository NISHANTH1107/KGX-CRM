from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Profile,Hackathon,Learnbypractice,Internship
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from .forms import HolidayForm
from .models import Holiday
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HolidayForm
from .models import Holiday
import threading
import subprocess
from .import generate_pdf,email_service



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
                return redirect('dashboard')  # Redirect to a home page or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    profile = get_object_or_404(Profile, roll_no=request.user.username)
    return render(request, 'profile.html', {'profile': profile})
    
@login_required
def learn_by_practice(request):
    learnbypractices = Learnbypractice.objects.all()
    return render(request, 'learn_by_practice.html', {'learnbypractices': learnbypractices})

@login_required
def wifi(request):
    return render(request, 'wifi.html')


@login_required
def work_on_holidays(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.save()

            # Generate PDF and send email
            pdf_filename = generate_pdf.generate_pdf([new_entry])  # Adapt generate_pdf for Django context
            #email_service.send_email(pdf_filename)  # Uncomment if email sending is needed

            # Generate and send access pass
            # access_pass.send_access_pass(new_entry)  # Adapt access_pass for Django context

            messages.success(request, 'Submitted Successfully!')
            return redirect('work_on_holidays')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = HolidayForm()

    return render(request, 'work_on_holidays.html', {'form': form})


@login_required
def hackathon(request):
    images = Hackathon.objects.all()
    return render(request, 'hackathon.html', {'images': images})

@login_required
def internship(request):
    internships = Internship.objects.all()  # Get all internships
    return render(request, 'internship.html', {'internships': internships})


@login_required
def inventory(request):
    return render(request, 'inventory.html')


@login_required
def contact_view(request):
    return render(request, 'contact.html')
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


    
