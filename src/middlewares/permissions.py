from rest_framework import permissions, exceptions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsOwnerOrPostOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user

        return obj.create_by == request.user


