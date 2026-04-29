from django.db import models
from django.conf import settings


class Elective(models.Model):
    """Represents an elective course with seat tracking."""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    total_seats = models.PositiveIntegerField(default=15)
    available_seats = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def seats_filled(self):
        return self.total_seats - self.available_seats

    @property
    def fill_percentage(self):
        if self.total_seats == 0:
            return 100
        return round((self.seats_filled / self.total_seats) * 100)

    @property
    def status(self):
        pct = self.fill_percentage
        if pct >= 100:
            return 'red'
        elif pct >= 70:
            return 'yellow'
        return 'green'


class Choice(models.Model):
    """Stores a student's ranked elective preferences (priority 1, 2, 3)."""
    PRIORITY_CHOICES = [(1, '1st Choice'), (2, '2nd Choice'), (3, '3rd Choice')]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    elective = models.ForeignKey(
        Elective,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('student', 'priority'),
            ('student', 'elective'),
        ]
        ordering = ['priority']

    def __str__(self):
        return f"{self.student.usn} → {self.elective.code} (Priority {self.priority})"
