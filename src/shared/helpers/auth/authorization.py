from uuid import UUID

from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


def require_admin(user_repo: IUserRepository, requester_user_id: UUID) -> None:
    requester = user_repo.get_user(requester_user_id)

    if requester.role != RoleEnum.ADMIN and requester.active != True:
        raise ForbiddenAction("user")
