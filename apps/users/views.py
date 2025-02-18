"""Users app views."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from apps.users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """User view set."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('last_name', 'email', 'groups')
    
    def get_permissions(self):
        """Asigna permisos especiales cuando se elimine uno o varios usuarios."""
        permissions = [IsAuthenticated]
        if self.action in ['create']:
            return []
        return [p() for p in permissions]
