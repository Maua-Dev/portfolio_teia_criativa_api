from typing import List
from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository

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

    def get_all_members(self) -> List[Member]:
        return self.members

    def create_member(self, member: Member) -> Member:
        self.members.append(member)
        return member