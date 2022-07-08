from rest_framework import permissions

class CustomIsTheAccountUser(permissions.BasePermission):
    def has_object_permission(self, request, _, obj):
        return request.user == obj

class CustomIsSuperuser(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.is_superuser