import uuid
from typing import Optional

from pydantic import ValidationError

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.controller_errors import MissingParameters


class UpdateMemberUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(
        self,
        member_id: str,
        new_member_photo: Optional[str] = None,
        new_member_name: Optional[str] = None,
        new_member_intro: Optional[str] = None,
    ) -> Member:
        try:
            parsed_id = uuid.UUID(member_id)
        except (ValueError, TypeError, AttributeError):
            raise EntityError("member_id")

        updates = {
            "new_member_photo": new_member_photo,
            "new_member_name": new_member_name,
            "new_member_intro": new_member_intro,
        }
        if not any(value is not None for value in updates.values()):
            raise MissingParameters(
                "new_member_photo, new_member_name, or new_member_intro"
            )

        for field_name, value in updates.items():
            if value is not None and type(value) is not str:
                raise EntityError(field_name)

        existing_member = self.repo.get_member(parsed_id)

        try:
            updated_member = Member(
                member_id=existing_member.member_id,
                member_photo=(
                    new_member_photo
                    if new_member_photo is not None
                    else existing_member.member_photo
                ),
                member_name=(
                    new_member_name
                    if new_member_name is not None
                    else existing_member.member_name
                ),
                member_intro=(
                    new_member_intro
                    if new_member_intro is not None
                    else existing_member.member_intro
                ),
            )
        except ValidationError as err:
            field_name = str(err.errors()[0]["loc"][0])
            raise EntityError(field_name) from err

        return self.repo.update_member(updated_member)
