"""Students app urls."""
from rest_framework.routers import DefaultRouter
from apps.students.views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = router.urls
