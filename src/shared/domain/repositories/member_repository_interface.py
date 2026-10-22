from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.shared.domain.entities.member import Member


class IMemberRepository(ABC):

    @abstractmethod
    def get_member(self, member_id: UUID) -> Member:
        """If the member is not found, raise NoItemsFound."""
        pass

    @abstractmethod
    def get_all_members(self) -> List[Member]:
        pass

    @abstractmethod
    def create_member(self, member: Member) -> Member:
        pass

    @abstractmethod
    def update_member(self, member: Member) -> Member:
        """If the member is not found, raise NoItemsFound."""
        pass