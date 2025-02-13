"""Teachers app urls."""
from rest_framework.routers import DefaultRouter
from apps.teachers.views import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teachers')

urlpatterns = router.urls
