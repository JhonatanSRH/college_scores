"""Teachers app models."""
from django.db import models

class Teacher(models.Model):
    """Teacher model."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        """String representation."""
        return f"{self.first_name} {self.last_name}"
