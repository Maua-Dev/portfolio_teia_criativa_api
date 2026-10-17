import uuid

import pytest

from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.entities.member import Member
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberRepositoryMock:
    def test_get_member(self):
        repo = MemberRepositoryMock()

        member = repo.get_member(repo.members[0].member_id)

        assert member == repo.members[0]

    def test_get_member_not_found(self):
        repo = MemberRepositoryMock()

        with pytest.raises(NoItemsFound, match="No items found for member_id"):
            repo.get_member(uuid.uuid4())

    def test_get_all_members(self):
        repo = MemberRepositoryMock()
        members = repo.get_all_members()
        assert len(members) == 2
        assert members[0].member_name == "Alice Silva"

    def test_create_member(self):
        repo = MemberRepositoryMock()
        new_member = Member(
            member_id="d28b3e21-0268-4682-825f-22a76f2ed621",
            member_photo="https://teiacriativa.com/assets/carlos.jpg",
            member_name="Carlos",
            member_intro="Engenheiro"
        )
        
        created_member = repo.create_member(new_member)
        members = repo.get_all_members()
        
        assert created_member.member_name == "Carlos"
        assert len(members) == 3