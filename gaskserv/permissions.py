from rest_framework import permissions
from rest_framework import compat
from gaskserv.models import TimeEntry


class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and compat.is_authenticated(request.user)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsEntryValidForEnd(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        le = request.query_params.get('last_entry', None)
        if request.method == 'PATCH' and obj.end_time is not None and le:
            return False
        return True


class HasAllEntriesValid(permissions.BasePermission):
    def has_permission(self, request, view):
        has_unfinished_time_entries = TimeEntry.objects.filter(end_time=None, owner=request.user.id)
        if has_unfinished_time_entries and request.method == 'POST':
            return False
        return True


class IsMemberOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if safe method
        if request.method in permissions.SAFE_METHODS:
            return True

        # if member of team
        for team in obj.teams.all():
            for member in team.members.all():
                if request.user == member:
                    return True

        # if owner
        return obj.owner == request.user
