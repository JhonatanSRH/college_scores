"""Students app views."""
from rest_framework import viewsets
from apps.students.models import Student
from apps.students.serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """Student view set."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ('last_name', 'email')
