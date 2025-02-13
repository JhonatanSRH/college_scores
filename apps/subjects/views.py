"""Subjects app views."""
from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.subjects.models import Subject, Registration
from apps.subjects.serializers import (SubjectSerializer, RegistrationSerializer, 
                                       MultipleSubjectsRegistrationSerializer,
                                       SubjectStudentsSerializer)

class SubjectViewSet(viewsets.ModelViewSet):
    """Subject view set."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filterset_fields = ('name', 'code', 'teacher')

    @action(detail=False, methods=['get'])
    def students(self, request):
        """Get Students per subject."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubjectStudentsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubjectStudentsSerializer(queryset, many=True)
        return Response(serializer.data)

class RegistrationViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """Registration view set."""
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filterset_fields = ('student', 'subject', 'is_approved')

    def list(self, request, *args, **kwargs):
        """List data and provide the score average"""
        queryset = self.filter_queryset(self.get_queryset())
        avg_score = queryset.aggregate(Avg('score'))['score__avg']
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                    'data': serializer.data,
                    'avg_score': avg_score
                })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
                'data': serializer.data,
                'avg_score': avg_score
            })

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        """Create multiple registrations."""
        serializer = MultipleSubjectsRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registrations = serializer.save()
        return Response(self.get_serializer(registrations, many=True).data)
