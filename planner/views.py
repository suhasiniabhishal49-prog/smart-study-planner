from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, IntegerField
import random

from .models import Subject, Task, Profile
from .forms import UserRegistrationForm, SubjectForm, TaskForm, ProfileForm


# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

def home(request):
    if request.user.is_authenticated:
        return redirect('planner:dashboard')
    return render(request, 'planner/home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('planner:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('planner:dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'planner/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('planner:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('planner:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'planner/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('planner:login')


# =============================================================================
# DASHBOARD
# =============================================================================

@login_required
def dashboard(request):
    today = timezone.localtime().date()
    all_tasks = Task.objects.filter(user=request.user)

    completed_tasks = all_tasks.filter(status='Completed').count()
    pending_tasks_qs = all_tasks.filter(status='Pending')
    overdue_tasks = pending_tasks_qs.filter(deadline__lt=timezone.now())
    today_tasks = pending_tasks_qs.filter(deadline__date=today)
    upcoming_tasks = pending_tasks_qs.filter(deadline__gte=timezone.now()).order_by('deadline')[:5]

    # 🔥 Reminder system
    due_reminders = Task.objects.filter(
        user=request.user,
        reminder_time__lte=timezone.now(),
        reminder_sent=False
    )

    motivational_quotes = [
        "Keep pushing — you're closer than you think!",
        "Small progress every day adds up to big results.",
    ]

    reminder_notifications = []
    pending_count = pending_tasks_qs.count()

    if due_reminders.exists():
        for task in due_reminders:
            quote = random.choice(motivational_quotes)
            text = f"Reminder: '{task.title}' is pending. {quote}"
            reminder_notifications.append({'text': text})
            task.reminder_sent = True
            task.save(update_fields=['reminder_sent'])
    else:
        if pending_count > 0:
            quote = random.choice(motivational_quotes)
            reminder_notifications.append({
                'text': f"You have {pending_count} pending tasks. {quote}"
            })

    context = {
        'total_tasks': all_tasks.count(),
        'completed_tasks': completed_tasks,
        'pending_count': pending_count,
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
        'upcoming_tasks': upcoming_tasks,
        'reminder_notifications': reminder_notifications,
    }

    return render(request, 'planner/dashboard.html', context)


# =============================================================================
# PROFILE
# =============================================================================

@login_required
def profile(request):
    total_tasks = Task.objects.filter(user=request.user).count()
    completed = Task.objects.filter(user=request.user, status='Completed').count()
    subjects_count = Subject.objects.filter(user=request.user).count()

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('planner:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'planner/profile.html', {
        'total_tasks': total_tasks,
        'completed': completed,
        'pending': total_tasks - completed,
        'subjects_count': subjects_count,
        'profile_form': form,
        'profile': profile,
    })


# =============================================================================
# TASK ADD/EDIT (FIXED VERSION)
# =============================================================================

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('planner:tasks')
    else:
        form = TaskForm(user=request.user)

    subjects_exist = Subject.objects.filter(user=request.user).exists()

    return render(request, 'planner/add_task.html', {
        'form': form,
        'subjects_exist': subjects_exist,
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('planner:tasks')
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'planner/add_task.html', {
        'form': form,
        'editing': True,
        'task': task,
        'subjects_exist': True,
    })
