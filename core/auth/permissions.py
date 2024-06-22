import logging
from rest_framework.permissions import BasePermission, SAFE_METHODS
from pdb import set_trace

logger = logging.getLogger(__name__)


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)
        elif view.basename == 'post-comment':
            if request.method == 'DELETE':
                return request.user.is_superuser or request.user in [obj.author, obj.post.author]
            return request.user.id == obj.author_id

        return False

    def has_permission(self, request, view):
        if view.basename in ["post"]:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)
        elif view.basename == 'post-comment':
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return True

        return False
