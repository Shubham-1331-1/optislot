from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm


def register_view(request):
    """Student registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            login(request, student)
            messages.success(request, f"Welcome, {student.first_name}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Student login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Logout and redirect to login."""
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """Student dashboard showing choices and allotment result."""
    from electives.models import Choice
    from allotment.models import Allotment

    choices = Choice.objects.filter(student=request.user).select_related('elective').order_by('priority')
    allotment = Allotment.objects.filter(student=request.user).select_related('elective').first()

    return render(request, 'users/dashboard.html', {
        'choices': choices,
        'allotment': allotment,
    })
