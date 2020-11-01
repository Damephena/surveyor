from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    
    '''Object-level permission to only allow `admin` edit or delete content.'''
    def has_object_permission(self, request, view, obj):
        message = 'Making changes to this file is not allowed.'

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff
