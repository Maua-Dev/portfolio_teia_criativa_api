from typing import List

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository


class GetAllMembersUsecase:
    def __init__(self, repo: IMemberRepository):
        self.repo = repo

    def __call__(self) -> List[Member]:
        return self.repo.get_all_members()
