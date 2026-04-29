import csv
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from .models import Allotment
from .algorithm import run_allotment


@staff_member_required
def admin_dashboard_view(request):
    """Admin dashboard: view all allotments, run algorithm, export CSV."""
    from electives.models import Choice
    from django.contrib.auth import get_user_model
    Student = get_user_model()

    allotments = Allotment.objects.select_related('student', 'elective').all()
    students = Student.objects.filter(is_staff=False, is_superuser=False).order_by('-cgpa')
    choices = Choice.objects.select_related('student', 'elective').all()

    context = {
        'allotments': allotments,
        'students': students,
        'choices': choices,
        'allotment_count': allotments.count(),
        'student_count': students.count(),
    }
    return render(request, 'allotment/admin_dashboard.html', context)


@staff_member_required
def run_allotment_view(request):
    """Trigger the allotment algorithm (POST only)."""
    if request.method == 'POST':
        result = run_allotment()
        messages.success(
            request,
            f"Allotment complete. Allotted: {result['allotted']}, "
            f"Unallotted: {result['unallotted']} out of {result['total']} students."
        )
    return redirect('admin_dashboard')


@staff_member_required
def revert_allotment_view(request):
    """
    Revert (undo) the allotment.
    GET  → confirmation page showing how many records will be deleted.
    POST → deletes all Allotment records and resets available_seats to total_seats.
    """
    from electives.models import Elective

    if request.method == 'POST':
        with transaction.atomic():
            count = Allotment.objects.count()
            Allotment.objects.all().delete()
            electives = Elective.objects.all()
            for e in electives:
                e.available_seats = e.total_seats
            Elective.objects.bulk_update(electives, ['available_seats'])

        messages.warning(request, f"Allotment reverted. {count} allotment(s) cleared and all seats reset.")
        return redirect('admin_dashboard')

    # GET — show confirmation page
    allotment_count = Allotment.objects.count()
    return render(request, 'allotment/revert_confirm.html', {'allotment_count': allotment_count})


@staff_member_required
def export_csv_view(request):
    """Export allotment results as a downloadable CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="optislot_allotments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'USN', 'Elective Code', 'Elective Name', 'CGPA', 'Allotted At'])

    allotments = Allotment.objects.select_related('student', 'elective').order_by(
        'elective__name', '-student__cgpa'
    )
    for a in allotments:
        writer.writerow([
            a.student.get_full_name(),
            a.student.usn,
            a.elective.code,
            a.elective.name,
            a.student.cgpa,
            a.allotted_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response
