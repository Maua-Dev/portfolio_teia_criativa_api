import uuid

from pydantic import HttpUrl

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository


class CreateMemberUsecase:
    def __init__(self, repo: IMemberRepository): 
        self.repo = repo

    def __call__(self, member_photo: HttpUrl, member_name: str, member_intro: str):
        member = Member(
            member_id=uuid.uuid4(),
            member_photo=member_photo,
            member_name=member_name,
            member_intro=member_intro
        )

        return self.repo.create_member(member)