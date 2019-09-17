from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


# примесь для проверки. Является ли пользователь создателем объекта
# если да то он может его изменить если нет бдет иключение
class IsOWnOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# если вдруг не рабтатет аутентификация через токен от Djoser
# class AllowOptionsAuthentication(IsAuthenticated):
#     def has_permission(self, request, view):
#         if request.method == 'OPTIONS':
#             return True
#         return request.user and request.user.is_authenticated