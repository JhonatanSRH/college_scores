"""Teachers app serializers."""
from rest_framework import serializers
from apps.teachers.models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    """Teacher serializer."""
    class Meta:
        """Meta class."""
        model = Teacher
        fields = '__all__'
        read_only_fields = ('id',)
