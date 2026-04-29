from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(AbstractUser):
    """
    Custom user model representing a student.
    Extends Django's AbstractUser with USN and CGPA fields.
    """
    usn = models.CharField(max_length=20, unique=True, verbose_name="USN")
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0,
        verbose_name="CGPA"
    )
    # timestamp is auto-tracked via date_joined from AbstractUser

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-cgpa', 'date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.usn})"
