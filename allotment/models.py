from django.db import models
from django.conf import settings
from electives.models import Elective


class Allotment(models.Model):
    """Stores the final allotment result for each student."""
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='allotment'
    )
    elective = models.ForeignKey(
        Elective,
        on_delete=models.CASCADE,
        related_name='allotments'
    )
    allotted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['elective__name', 'student__cgpa']

    def __str__(self):
        return f"{self.student.usn} → {self.elective.code}"
