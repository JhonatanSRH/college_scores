"""Subjects app serializers."""
from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.validators import ValidationError
from apps.subjects.models import Subject, Registration
from apps.users.models import User
from apps.users.serializers import UserSerializer

class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer."""
    class Meta:
        """Meta class."""
        model = Subject
        fields = '__all__'
        read_only_fields = ('id',)

class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer."""
    student = UserSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Registration
        depth = 1
        fields = '__all__'
        read_only_fields = ('id', 'student', 'subject', 'is_approved')

    def validate_score(self, value):
        """Validate score"""
        if value and 0 <= value <= 5:
            return value
        raise ValidationError('The score must be a value between 0 and 5')

    def validate(self, data):
        """Validate if there is a previous score"""
        if 'score' in data:
            if self.instance.score:
                raise ValidationError({'score': 'The score has been submitted already.'})
        return super().validate(data)

    def save(self, **kwargs):
        """Update is_approved depending on the value of the score"""
        validated_data = self.validated_data
        if validated_data.get('score'):
            validated_data['is_approved'] = validated_data['score'] >= 3
        # Llamar al método save original para guardar el objeto
        return super().save(**kwargs)

class RegistrationStudentSerializer(serializers.ModelSerializer):
    """Registration Student serializer."""
    student = UserSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Registration
        fields = ('id', 'student', 'is_approved', 'score')

class SubjectStudentsSerializer(serializers.ModelSerializer):
    """Subject Student serializer."""
    teacher = UserSerializer(read_only=True)
    registrations = serializers.SerializerMethodField()
    
    def get_registrations(self, obj):
        registrations = obj.registrations.all()
        return RegistrationStudentSerializer(registrations, many=True).data
    
    class Meta:
        """Meta class."""
        model = Subject
        fields = ('id', 'teacher', 'registrations', 'name', 'code')

class MultipleSubjectsRegistrationSerializer(serializers.Serializer):
    """Multiple Subjects Registration serializer."""
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True)
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, required=True)

    def validate(self, data):
        """Validate previous subjects approval."""
        student = data.get('student')
        subjects = data.get('subjects')
        for subject in subjects:
            previous_subjects = subject.previous_subjects.all()
            if previous_subjects:
                approved_subjects = Registration.objects.filter(
                    student=student, subject__in=previous_subjects, is_approved=True
                ).exists()
                if not approved_subjects:
                    subjects_names = (subject.name for subject in subject.previous_subjects.all())
                    raise serializers.ValidationError(
                        {
                        'subjects': ("The student hasn't approved "
                                    f"the subject(s) '{", ".join(subjects_names)}' yet.")}
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
