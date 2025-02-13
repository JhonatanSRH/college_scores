"""Subjects app urls."""
from rest_framework.routers import DefaultRouter
from apps.subjects.views import SubjectViewSet, RegistrationViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'registrations', RegistrationViewSet, basename='registrations')

urlpatterns = router.urls
