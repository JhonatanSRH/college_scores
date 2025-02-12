"""Students app models."""
from django.db import models

class Student(models.Model):
    """Student model."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()

    def __str__(self):
        """String representation."""
        return f"{self.first_name} {self.last_name}"
