from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,HolidayForm,CommentForm,WifiForm
from django.views.decorators.csrf import csrf_protect ,csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile,Learnbypractice,Internship,Holiday,Comment,Wifi,ToDo,InProgress,ForReview,Done
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError ,ObjectDoesNotExist
from .import generate_pdf,email_service
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta
from django.templatetags.static import static
from .decorators import role_required
import base64
import requests
from .utils import generate_wifi_report
from django.utils.decorators import method_decorator
from kgx_app.models import Profile
from django.db.models import Q

def home_redirect(request):
    if request.user.is_authenticated:
        try:
            # Attempt to get the profile based on the roll number (username)
            profile = Profile.objects.get(roll_no=request.user.username)
            # Redirect to the appropriate dashboard based on the role
            if profile.role == 'staff':
                return redirect('staff_dashboard')
            else:
                return redirect('dashboard')
        except Profile.DoesNotExist:
            # If no profile exists for the user, redirect to profile creation page
            return redirect('land/')
    else:
        # If not logged in, redirect to the login page
        return redirect('land/')

# views.py

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Assuming this is roll_no
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Fetch the profile using roll_no
                try:
                    profile = Profile.objects.get(roll_no=username)
                    
                    # Redirect based on role
                    if profile.role == Profile.STAFF:
                        return redirect('staff_dashboard')  # Redirect to staff dashboard
                    else:
                        return redirect('dashboard')  # Redirect to student dashboard
                
                except Profile.DoesNotExist:
                    messages.error(request, 'Profile not found.')
                    return redirect('login')
                
                messages.success(request, 'Login successful.')
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
@role_required(allowed_roles=['student'])
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
@role_required(allowed_roles=['student'])
def profile(request):
    profile = get_object_or_404(Profile, roll_no=request.user.username)
    return render(request, 'profile.html', {'profile': profile})
    

@login_required
@role_required(allowed_roles=['student'])
def student_tasks(request):
    # Get the profile of the currently logged-in student
    profile = get_object_or_404(Profile, roll_no=request.user.username)

    # Retrieve tasks for the student using their roll number
    to_do_tasks = ToDo.objects.filter(roll_no=profile.roll_no)  # Use the roll number from the profile
    in_progress_tasks = InProgress.objects.filter(roll_no=profile.roll_no)
    for_review_tasks = ForReview.objects.filter(roll_no=profile.roll_no)
    done_tasks = Done.objects.filter(roll_no=profile.roll_no) 

    # Render the student tasks page with the tasks retrieved
    return render(request, 'student_tasks.html', {
        'profile': profile,
        'to_do_tasks': to_do_tasks,
        'in_progress_tasks': in_progress_tasks,
        'for_review_tasks': for_review_tasks,
        'done_tasks': done_tasks,
    })
    
@login_required
@role_required(allowed_roles=['student'])
def wifi_view(request):
    if request.method == 'POST':
        roll_no_input = request.POST.get('roll_no')  # Get the roll number from the form
        try:
            # Check if the roll number exists in the Profile model
            roll_no_instance = Profile.objects.get(roll_no=roll_no_input)  # Query Profile instead
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'message': "User not found."})  # Send error response

        # Create a new Wifi instance directly from the form data
        wifi_instance = Wifi(
            roll_no=roll_no_instance,  # Use the found Profile instance
            mac_address=request.POST.get('mac_address'),
            screenshot=request.FILES.get('screenshot'),  # Get the uploaded screenshot
        )

        try:
            wifi_instance.save()  # Save the Wifi instance to the database
            
            # Call the report generation function and pass the user's email
            generate_wifi_report(roll_no_instance.user.email)  # Assuming user email is accessible
            
            return JsonResponse({'success': True})  # Send a success response
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})  # Send error response

    # If the request is GET, just render the form
    return render(request, 'wifi.html')

@login_required
@role_required(allowed_roles=['student'])
def work_on_holidays(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        print(f"Form valid: {form.is_valid()}")  # Check if form is valid
        print(f"Form errors: {form.errors}")  # Output any form errors
        if form.is_valid():
            new_entry = form.save(commit=False)
            print(f"Saving new entry: {new_entry}")  # Check the object before saving
            new_entry.save()
            print(f"Saved new entry: {new_entry.id}")  # Check if the save was successful

            # Generate PDF and send email
            pdf_filename = generate_pdf.generate_pdf([new_entry])  
            messages.success(request, 'Submitted Successfully!')
            return redirect('work_on_holidays')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = HolidayForm()

    return render(request, 'work_on_holidays.html', {'form': form})

@login_required
@role_required(allowed_roles=['student'])
def internship(request):
    internships = Internship.objects.all()  # Get all internships
    return render(request, 'internship.html', {'internships': internships})

@login_required
@role_required(allowed_roles=['student'])
def contact_view(request):
    return render(request, 'contact.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')

@login_required
@require_POST
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
                profile_image = (
                    new_comment.user.profile.image.url
                    if hasattr(new_comment.user, 'profile') and new_comment.user.profile.image
                    else static('kgx_app/default_profile.png')  # Use default image if profile or image doesn't exist
                )

                return JsonResponse({'success': True, 'comment': content, 'profile_image': profile_image})
            else:
                return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
@role_required(allowed_roles=['staff'])
def staff_dashboard(request):
    # Logic for staff dashboard
    return render(request, 'staff_dashboard.html')


@login_required
@role_required(allowed_roles=['staff'])
def assign_task(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')
        name = request.POST.get('name')
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')
        reference_link = request.POST.get('reference_link')
        due_date = request.POST.get('due_date')
        
        # Save the task to the ToDo model
        ToDo.objects.create(
            roll_no=roll_no,
            name=name,
            task_title=task_title,
            task_description=task_description,
            reference_link=reference_link,
            due_date=due_date
        )
        
        messages.success(request, 'Task assigned successfully!')
        return redirect('assign_task')  # Redirect to the same page or another page after submission

    return render(request, 'assign_task.html')

@login_required
def start_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(ToDo, id=task_id)
        in_progress_task = InProgress(
            task_title=task.task_title,
            task_description=task.task_description,
            due_date=task.due_date,
            reference_link=task.reference_link,
            roll_no=task.roll_no,
            name=task.name  # Assuming roll_no is a field to associate with users
        )
        in_progress_task.save()
        task.delete()  # Remove from ToDo
        return redirect('student_tasks')

    return redirect('student_tasks')


@login_required
@role_required(allowed_roles=['student'])  # Only students should access this
def submit_task_link(request, task_id):
    if request.method == 'POST':
        task_link = request.POST.get('task_link')
        
        # Get the task from InProgress model
        task = get_object_or_404(InProgress, id=task_id)
        
        # Create a new ForReview instance
        ForReview.objects.create(
            roll_no=task.roll_no,
            name=task.name,
            task_title=task.task_title,
            task_description=task.task_description,
            reference_link=task.reference_link,
            task_link=task_link,  # The link provided by the student
            due_date=task.due_date
        )
        
        # Remove the task from InProgress
        task.delete()
        
        return redirect('student_tasks')  # Redirect back to the tasks page
    


@login_required
@role_required(allowed_roles=['staff'])  # Ensure only staff can access this view
def to_do_list(request):
    to_do_tasks = ToDo.objects.all()  # Retrieve all tasks from the ToDo model
    return render(request, 'staff/to_do_list.html', {'to_do_tasks': to_do_tasks})

# In Progress View
@login_required
@role_required(allowed_roles=['staff'])
def in_progress(request):
    # Logic for displaying tasks that are in progress
    return render(request, 'in_progress.html')

@login_required
@role_required(allowed_roles=['staff'])
def for_review(request):
    # Fetch tasks in the For Review model
    for_review_tasks = ForReview.objects.all()

    return render(request, 'for_review.html', {'for_review_tasks': for_review_tasks})

@login_required
@role_required(allowed_roles=['staff'])
def review_task(request, task_id):
    task = get_object_or_404(ForReview, id=task_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'correct':
            # Move to Done model
            Done.objects.create(
                roll_no=task.roll_no,
                name=task.name,
                task_title=task.task_title,
                task_description=task.task_description,
                reference_link=task.reference_link,
                due_date=task.due_date,
                task_link=task.task_link  # Include task link in Done model
            )
            task.delete()  # Delete from ForReview model

        elif action == 'wrong':
            # Move back to ToDo model
            ToDo.objects.create(
                roll_no=task.roll_no,
                name=task.name,
                task_title=task.task_title,
                task_description=task.task_description,
                reference_link=task.reference_link,
                due_date=task.due_date
            )
            task.delete()  # Delete from ForReview model

        return redirect('for_review')
    
@login_required
@role_required(allowed_roles=['staff'])
def to_do_view(request):
    to_do_tasks = ToDo.objects.all()  # Retrieve all tasks from ToDo
    return render(request, 'to_do.html', {'to_do_tasks': to_do_tasks})

@login_required
@role_required(allowed_roles=['staff'])
def in_progress_view(request):
    in_progress_tasks = InProgress.objects.all()  # Retrieve all tasks from InProgress
    return render(request, 'in_progress.html', {'in_progress_tasks': in_progress_tasks})

@login_required
@role_required(allowed_roles=['staff'])
def done_view(request):
    done_tasks = Done.objects.all()  # Retrieve all tasks from Done
    return render(request, 'done.html', {'done_tasks': done_tasks})


def landing_page(request):
    return render(request, 'landingpg.html')

@csrf_exempt
@login_required
@role_required(allowed_roles=['staff'])
def search_names(request):
    query = request.GET.get('q', '')
    if query:
        profiles = Profile.objects.filter(name__icontains=query)[:5]  # Limit to 5 suggestions
        name_list = list(profiles.values_list('name','roll_no'))  # Extract only the names
    else:
        name_list = []
    
    return JsonResponse(name_list, safe=False)