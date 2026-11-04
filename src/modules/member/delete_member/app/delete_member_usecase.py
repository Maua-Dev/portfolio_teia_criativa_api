import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class DeleteMemberUsecase:
    def __init__(self, repo: IMemberRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self, member_id: str, requester_id: str | None) -> Member:
        try:
            parsed_requester_id = uuid.UUID(requester_id)
        except (ValueError, TypeError, AttributeError):
            raise EntityError("requester_id")

        requester = self.user_repo.get_user(user_id=parsed_requester_id)
        if (
            requester is None
            or not requester.active
            or requester.role != RoleEnum.ADMIN
        ):
            raise ForbiddenAction("Delete Member")

        try:
            parsed_member_id = uuid.UUID(member_id)
        except (ValueError, TypeError, AttributeError):
            raise EntityError("member_id")

        member = self.repo.delete_member(parsed_member_id)
        if member is None:
            raise NoItemsFound("member_id")

        return member
