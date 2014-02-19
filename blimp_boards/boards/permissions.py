from rest_framework import permissions

from ..accounts.models import AccountCollaborator
from .models import Board


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator with the
        corresponding permission on this board, `False` otherwise.
        """
        permission = 'read'

        if request.method not in permissions.SAFE_METHODS:
            permission = 'write'

        return obj.is_user_collaborator(request.user, permission=permission)


class BoardCollaboratorPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        """
        Returns `True` if the user is a board collaborator with
        write permissions trying to create. Returns `True` if
        user is the account owner.
        """
        is_authenticated = request.user and request.user.is_authenticated()

        if not is_authenticated:
            return False

        board_id = request.DATA.get('board')

        if request.method == 'POST' and board_id:
            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                return False

            permission = BoardPermission()
            has_board_permission = permission.has_object_permission(
                request, view, board)

            account_owner = AccountCollaborator.objects.filter(
                account_id=board.account_id,
                user=request.user,
                is_owner=True
            )

            return has_board_permission or account_owner.exists()

        return True

    def has_object_permission(self, request, view, obj):
        """
        Returns `True` if user is a board collaborator with write permissions.
        Returns `True` if user is the board collaborator trying to delete.
        Returns `True if user is the account owner.
        """

        if request.method == 'DELETE':
            has_board_permission = request.user == obj.user
        else:
            permission = BoardPermission()
            has_board_permission = permission.has_object_permission(
                request, view, obj.board)

        account_owner = AccountCollaborator.objects.filter(
            account_id=obj.board.account_id,
            user=request.user,
            is_owner=True
        )

        return has_board_permission or account_owner.exists()


class BoardCollaboratorRequestPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if user is a collaborator with the
        corresponding permission on this board, `False` otherwise.
        """
        return obj.board.account.is_user_collaborator(
            request.user, is_owner=True)