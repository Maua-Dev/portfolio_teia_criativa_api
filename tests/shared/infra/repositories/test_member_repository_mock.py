import uuid

import pytest

from src.shared.domain.entities.member import Member
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberRepositoryMock:
    def test_get_member(self):
        repo = MemberRepositoryMock()

        member = repo.get_member(uuid.UUID("f4019bd7-52d3-463d-8ab1-1d373c004a43"))

        assert member.member_id == uuid.UUID("f4019bd7-52d3-463d-8ab1-1d373c004a43")
        assert member.member_name == "Alice Silva"

    def test_get_member_not_found(self):
        repo = MemberRepositoryMock()

        with pytest.raises(NoItemsFound):
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

    def test_delete_member(self):
        repo = MemberRepositoryMock()

        member = repo.delete_member(uuid.UUID("f4019bd7-52d3-463d-8ab1-1d373c004a43"))

        assert member.member_name == "Alice Silva"
        assert len(repo.members) == 1

    def test_delete_member_not_found(self):
        repo = MemberRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_member(uuid.uuid4())

    def test_update_member(self):
        repo = MemberRepositoryMock()
        updated = Member(
            member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
            member_photo="https://teiacriativa.com/assets/alice-updated.jpg",
            member_name="Alice Souza",
            member_intro="Tech Lead"
        )

        member = repo.update_member(updated)

        assert member.member_name == "Alice Souza"
        assert repo.members[0].member_name == "Alice Souza"

    def test_update_member_not_found(self):
        repo = MemberRepositoryMock()
        non_existent_member = Member(
            member_id=uuid.uuid4(),
            member_photo="https://teiacriativa.com/assets/unknown.jpg",
            member_name="Unknown",
            member_intro="Unknown"
        )

        with pytest.raises(NoItemsFound):
            repo.update_member(non_existent_member)
