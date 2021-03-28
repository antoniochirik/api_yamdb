from rest_framework import permissions


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_admin
                or request.user.is_superuser)
