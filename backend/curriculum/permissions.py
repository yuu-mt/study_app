from rest_framework import permissions


class IsInstructorOrAdmin(permissions.BasePermission):
    """管理画面へのアクセスは instructor / admin ロールのみ許可する（要件定義書 6.）"""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and user.role in ('instructor', 'admin')
        )


class IsAdminRole(permissions.BasePermission):
    """カリキュラム編集・講師ロール付与など admin 専用の操作を許可する
    （要件定義書 3-1-b・3-3 参照）。
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == 'admin')


class IsAdminOrReadOnlyForInstructor(permissions.BasePermission):
    """カリキュラム管理画面用：instructor は閲覧のみ、admin は編集・削除・並び替えも可能
    （要件定義書 3-3 参照）。閲覧できるのはinstructor/admin両ロールのみ。
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated and user.role in ('instructor', 'admin')):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return user.role == 'admin'
