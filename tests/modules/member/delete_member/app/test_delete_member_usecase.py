import uuid

import pytest

from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestDeleteMemberUsecase:
    def test_delete_member(self):
        repo = MemberRepositoryMock()
        original_member = repo.members[0]
        member_count = len(repo.members)

        deleted_member = DeleteMemberUsecase(repo)(str(original_member.member_id))

        assert deleted_member == original_member
        assert len(repo.members) == member_count - 1
        assert original_member not in repo.members

    def test_delete_member_not_found(self):
        with pytest.raises(NoItemsFound):
            DeleteMemberUsecase(MemberRepositoryMock())(str(uuid.uuid4()))

    @pytest.mark.parametrize("member_id", ["not-a-uuid", None, 123])
    def test_delete_member_invalid_id(self, member_id):
        with pytest.raises(EntityError, match="Field member_id is not valid"):
            DeleteMemberUsecase(MemberRepositoryMock())(member_id)
