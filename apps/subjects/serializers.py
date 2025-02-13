"""Subjects app serializers."""
from django.db import transaction, IntegrityError
from rest_framework import serializers
from apps.subjects.models import Subject, Registration
from apps.students.models import Student

class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer."""
    class Meta:
        """Meta class."""
        model = Subject
        fields = '__all__'
        read_only_fields = ('id',)

class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer."""
    class Meta:
        """Meta class."""
        model = Registration
        depth = 1
        fields = '__all__'
        read_only_fields = ('id',)

class MultipleSubjectsRegistrationSerializer(serializers.Serializer):
    """Multiple Subjects Registration serializer."""
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), required=True)
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, required=True)

    def validate(self, data):
        """Validate previous subjects approval."""
        student = data.get('student')
        subjects = data.get('subjects')
        for subject in subjects:
            previous_subjects = subject.previous_subjects.all()
            for previous_subject in previous_subjects:
                if not Registration.objects.filter(student=student, subject=previous_subject, is_approved=True).exists():
                    raise serializers.ValidationError(
                        {'subjects': f"The student hasn't approved the subject '{previous_subject.name}' yet."}
                    )
        return data

    def create(self, validated_data):
        """Create multiple registrations."""
        student = validated_data.get('student')
        subjects = validated_data.get('subjects')
        try:
            with transaction.atomic():
                registrations = Registration.objects.bulk_create(
                    Registration(student=student, subject=subject) for subject in subjects)
        except IntegrityError as error:
            msg = str(error)
            if 'UNIQUE constraint failed' in msg:
                msg = 'This student has those subjects (or one of them) already registered.'
            raise serializers.ValidationError({'subjects': msg})
        return registrations
