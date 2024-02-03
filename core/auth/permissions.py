from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["post"]:
            return bool(request.user and request.user.is_authenticated)
        if view.basename in ["post-comment"] : 
            if request.method in ['DELETE']:
                return bool(request.user.is_superuser or request.user in [obj.author, obj.post.author])

            return bool(request.user and request.user.is_authenticated)
        elif view.basename == "comment":
        # Добавляем проверку разрешения для редактирования комментария
            if request.method == "PUT":
                
                return request.user.has_perm('change_comment', obj)


        return False

    def has_permission(self, request, view):
        if view.basename in ["post", "post-comment"]:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)

        return False
