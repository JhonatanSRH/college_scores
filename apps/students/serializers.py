"""Students app serializers."""
from rest_framework import serializers
from apps.students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer."""
    class Meta:
        """Meta class."""
        model = Student
        fields = '__all__'
        read_only_fields = ('id',)
