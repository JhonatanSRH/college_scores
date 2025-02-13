"""Teachers app views."""
from rest_framework import viewsets
from apps.teachers.models import Teacher
from apps.teachers.serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """Teacher view set."""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = ('last_name', 'email')
