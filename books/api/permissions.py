from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsCommentAuthorOrReadOnly(CustomPermission):
    """ Permission позводяющий создавать и изменять обекты комментариев только автору """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                )


class IsBookAuthorOrReadOnly(CustomPermission):
    """ Permission позводяющий создавать и изменять обекты книг только автору """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user in obj.authors.all()
                )


class IsCurrentUserOrReadOnly(CustomPermission):
    """ Permission позводяющий создавать и изменять обекты пользователя только самого себя """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj
                )
