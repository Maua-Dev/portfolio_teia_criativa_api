from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.shared.domain.entities.member import Member


class IMemberRepository(ABC):
    
    @abstractmethod
    def get_member(self, member_id: UUID) -> Member:
        """Return the member or raise NoItemsFound when it does not exist."""
        pass

    @abstractmethod
    def get_all_members(self) -> List[Member]:
        pass

    @abstractmethod
    def create_member(self, member: Member) -> Member:
        pass