from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,HolidayForm,CommentForm
from django.views.decorators.csrf import csrf_protect ,csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile,Hackathon,Learnbypractice,Internship,Holiday,Comment
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .import generate_pdf,email_service
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta
from django.templatetags.static import static

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if logged in
    else:
        return redirect('login')  # Redirect to the login page if not logged in


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
    comments = Comment.objects.select_related('user').all().order_by('-created_at')  # Fetch comments with user profile
    for comment in comments:
        try:
            # Assuming the username is the roll number
            profile = Profile.objects.get(roll_no=comment.user.username)
            comment.profile_image_url = profile.image.url if profile.image else '/static/kgx_app/default_profile.png'
        except Profile.DoesNotExist:
            comment.profile_image_url = '/static/kgx_app/default_profile.png'  # Default image if profile does not exist

   # Calculate the time 24 hours ago
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

    # Filter comments created in the last 24 hours
    recent_comments = Comment.objects.filter(created_at__gte=twenty_four_hours_ago)

    return render(request, 'dashboard.html', {'comments': recent_comments})

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

@login_required
@require_POST
@csrf_exempt  # Use for testing, but ideally, keep CSRF protection enabled in production
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            if content:
                # Create a new comment in your Comment model
                new_comment = Comment(user=request.user, content=content)  # Associate with the logged-in user
                new_comment.save()
                
                # Prepare response data
               
                #response_data = {
                #    'success': True,
                #   'comment': content,
                #    'profile_image': new_comment.user.profile.image.url if new_comment.user.profile.image else static('kgx_app/default_profile.png')
                #}
            
                return JsonResponse({'success': True, 'comment': content})
            else:
                return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})