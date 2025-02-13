"""Subjects app views."""
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.subjects.models import Subject, Registration
from apps.subjects.serializers import (SubjectSerializer, RegistrationSerializer, 
                                       MultipleSubjectsRegistrationSerializer)

class SubjectViewSet(viewsets.ModelViewSet):
    """Subject view set."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filterset_fields = ('name', 'code', 'teacher')

class RegistrationViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """Registration view set."""
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filterset_fields = ('student', 'subject')

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        """Create multiple registrations."""
        serializer = MultipleSubjectsRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registrations = serializer.save()
        return Response(self.get_serializer(registrations, many=True).data)
