"""Subjects app models."""
from django.db import models

class Subject(models.Model):
    """Subject model."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(
        'teachers.Teacher', on_delete=models.CASCADE, related_name='subjects')
    previous_subjects = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='requirements')

    def __str__(self):
        """String representation."""
        return f"{self.name}"

class Registration(models.Model):
    """Registration model."""
    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name='registrations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateField(auto_now_add=True)
    score = models.FloatField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        """String representation."""
        return f"{self.student} - {self.subject}"

    class Meta:
        unique_together = ('student', 'subject')
