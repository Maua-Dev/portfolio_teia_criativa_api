import uuid

import pytest

from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestUpdateMemberUsecase:
    def test_partial_update_preserves_other_fields(self):
        repo = MemberRepositoryMock()
        original = repo.members[0]

        updated = UpdateMemberUsecase(repo)(
            member_id=str(original.member_id),
            new_member_name="Alice Silva Santos",
        )

        assert updated.member_name == "Alice Silva Santos"
        assert updated.member_photo == original.member_photo
        assert updated.member_intro == original.member_intro
        assert repo.get_member(original.member_id) == updated

    def test_update_multiple_fields(self):
        repo = MemberRepositoryMock()

        updated = UpdateMemberUsecase(repo)(
            member_id=str(repo.members[0].member_id),
            new_member_name="Updated Alice",
            new_member_intro="Product Designer",
        )

        assert updated.member_name == "Updated Alice"
        assert updated.member_intro == "Product Designer"

    def test_rejects_invalid_member_id(self):
        with pytest.raises(EntityError, match="Field member_id is not valid"):
            UpdateMemberUsecase(MemberRepositoryMock())(
                member_id="invalid",
                new_member_name="New name",
            )

    def test_rejects_invalid_photo(self):
        repo = MemberRepositoryMock()

        with pytest.raises(EntityError, match="Field member_photo is not valid"):
            UpdateMemberUsecase(repo)(
                member_id=str(repo.members[0].member_id),
                new_member_photo="https://example.com/photo.png",
            )

    def test_requires_at_least_one_field(self):
        repo = MemberRepositoryMock()

        with pytest.raises(MissingParameters):
            UpdateMemberUsecase(repo)(member_id=str(repo.members[0].member_id))

    def test_rejects_unknown_member(self):
        with pytest.raises(NoItemsFound):
            UpdateMemberUsecase(MemberRepositoryMock())(
                member_id=str(uuid.uuid4()),
                new_member_name="New name",
            )
