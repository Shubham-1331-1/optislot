from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Elective, Choice
from .forms import ChoiceForm


@login_required
def elective_list_view(request):
    """Show all electives with live seat status."""
    electives = Elective.objects.all()
    return render(request, 'electives/list.html', {'electives': electives})


@login_required
def submit_choices_view(request):
    """Allow student to submit their top 3 elective choices."""
    student = request.user

    # Check if allotment has already run — lock choices after that
    from allotment.models import Allotment
    allotment_done = Allotment.objects.exists()
    existing_choices = Choice.objects.filter(student=student).order_by('priority')

    if request.method == 'POST':
        if allotment_done:
            messages.error(request, "Allotment has already been run. Choices are locked.")
            return redirect('dashboard')

        form = ChoiceForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Delete old choices and replace
                Choice.objects.filter(student=student).delete()
                for i, key in enumerate(['choice_1', 'choice_2', 'choice_3'], start=1):
                    Choice.objects.create(
                        student=student,
                        elective=form.cleaned_data[key],
                        priority=i
                    )
            messages.success(request, "Your choices have been saved successfully.")
            return redirect('dashboard')
    else:
        # Pre-fill form if choices exist
        initial = {}
        for choice in existing_choices:
            initial[f'choice_{choice.priority}'] = choice.elective
        form = ChoiceForm(initial=initial)

    return render(request, 'electives/submit_choices.html', {
        'form': form,
        'allotment_done': allotment_done,
        'existing_choices': existing_choices,
    })
