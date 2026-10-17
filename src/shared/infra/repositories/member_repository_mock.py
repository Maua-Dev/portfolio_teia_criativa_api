from typing import List
from uuid import UUID

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class MemberRepositoryMock(IMemberRepository):
    members: List[Member]

    def __init__(self):
        self.members = [
            Member(
                member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
                member_photo="https://teiacriativa.com/assets/alice.jpg",
                member_name="Alice Silva",
                member_intro="Desenvolvedora Backend"
            ),
            Member(
                member_id="a9a95726-5b82-4148-8df0-1c6ba52f7f9f",
                member_photo="https://teiacriativa.com/assets/bob.jpg",
                member_name="Bob Santos",
                member_intro="UI/UX Designer"
            )
        ]

    def get_member(self, member_id: UUID) -> Member:
        for member in self.members:
            if str(member.member_id) == str(member_id):
                return member
        raise NoItemsFound("member_id")

    def get_all_members(self) -> List[Member]:
        return self.members

    def create_member(self, member: Member) -> Member:
        self.members.append(member)
        return member