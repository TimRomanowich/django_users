from rest_framework import permissions
from .models import ChatPrivilege

class HasChatPrivileges(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            privileges = request.user.chatprivilege
            if view.action == 'list' or view.action == 'retrieve':
                return privileges.can_read
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                return privileges.can_post
        except ChatPrivilege.DoesNotExist:
            return False
        return False

class CanPostMedia(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.chatprivilege.can_post_media
        except ChatPrivilege.DoesNotExist:
            return False