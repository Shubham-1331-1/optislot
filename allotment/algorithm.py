"""
OptiSlot Ranked-Choice Allotment Algorithm
==========================================
Allocation logic:
  1. Sort students by CGPA (desc), then by registration timestamp (asc).
  2. For each student, try to allocate their 1st choice.
     If full → try 2nd choice → try 3rd choice → mark as unallotted.
  3. All seat decrements happen inside a single atomic transaction
     with select_for_update() to prevent race conditions.

Returns a summary dict with counts of allotted/unallotted students.
"""

import logging
from django.db import transaction
from django.conf import settings

from electives.models import Elective, Choice
from .models import Allotment

logger = logging.getLogger(__name__)

Student = None  # lazy import to avoid circular imports


def run_allotment():
    """
    Execute the full ranked-choice allotment algorithm.
    Safe to call multiple times — clears previous results first.
    Returns: dict with 'allotted', 'unallotted', 'total' counts.
    """
    from django.contrib.auth import get_user_model
    StudentModel = get_user_model()

    allotted_count = 0
    unallotted_students = []

    with transaction.atomic():
        # 1. Clear previous allotment results
        Allotment.objects.all().delete()

        # 2. Reset available_seats to total_seats for all electives
        #    Lock all elective rows to prevent concurrent modification
        electives = Elective.objects.select_for_update().all()
        for elective in electives:
            elective.available_seats = elective.total_seats
        Elective.objects.bulk_update(electives, ['available_seats'])

        # 3. Get all students sorted by CGPA desc, then registration time asc
        students = StudentModel.objects.filter(
            is_staff=False, is_superuser=False
        ).order_by('-cgpa', 'date_joined')

        # 4. Process each student in priority order
        for student in students:
            choices = Choice.objects.filter(student=student).order_by('priority')

            if not choices.exists():
                logger.info(f"Student {student.usn} has no choices — skipping.")
                unallotted_students.append(student.usn)
                continue

            allocated = False

            for choice in choices:
                # Re-fetch elective with row lock to prevent race conditions
                try:
                    elective = Elective.objects.select_for_update().get(pk=choice.elective_id)
                except Elective.DoesNotExist:
                    continue

                if elective.available_seats > 0:
                    # Allocate this elective to the student
                    elective.available_seats -= 1
                    elective.save(update_fields=['available_seats'])

                    Allotment.objects.create(student=student, elective=elective)
                    allotted_count += 1
                    allocated = True
                    logger.info(
                        f"Allotted {student.usn} → {elective.code} "
                        f"(Priority {choice.priority}, CGPA {student.cgpa})"
                    )
                    break  # stop trying further choices

            if not allocated:
                unallotted_students.append(student.usn)
                logger.warning(f"Student {student.usn} could not be allotted any elective.")

    total = allotted_count + len(unallotted_students)
    return {
        'allotted': allotted_count,
        'unallotted': len(unallotted_students),
        'unallotted_usns': unallotted_students,
        'total': total,
    }
