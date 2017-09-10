from rest_framework import permissions
from rest_framework import compat

class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and compat.is_authenticated(request.user)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

class IsMemberOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #if safe method
        if request.method in permissions.SAFE_METHODS:
            return True

        #if member of team
        for team in obj.teams.all():
            for member in team.members.all():
                if request.user == member:
                    return True

        #if owner
        return obj.owner == request.user