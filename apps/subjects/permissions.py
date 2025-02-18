from rest_framework.permissions import BasePermission

class IsSubjectTeacher(BasePermission):
    """Is Subject Teacher Permission."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if hasattr(obj, 'teacher'):
                return obj.teacher == request.user
            elif hasattr(obj, 'subject'):
                return obj.subject.teacher == request.user
        return False

class IsTeacher(BasePermission):
    """Is Teacher Permission."""
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name='teachers').exists():
                if request.method == 'POST':
                    return request.data.get('teacher') == request.user.id
                elif request.method == 'GET':
                    return request.query_params.get('teacher') == str(request.user.id)
                else:
                    return True
        return False

class IsStudent(BasePermission):
    """Is Student Permission."""
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name='students').exists():
                if request.method == 'POST':
                    return request.data.get('student') == request.user.id
                elif request.method == 'GET':
                    return request.query_params.get('student') == str(request.user.id)
                else:
                    return True
        return False
