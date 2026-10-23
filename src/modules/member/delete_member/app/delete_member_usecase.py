import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class DeleteMemberUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(self, member_id: str) -> Member:
        try:
            parsed_id = uuid.UUID(member_id)
        except (ValueError, TypeError, AttributeError):
            raise EntityError("member_id")

        member = self.repo.delete_member(parsed_id)
        if member is None:
            raise NoItemsFound("member_id")

        return member
