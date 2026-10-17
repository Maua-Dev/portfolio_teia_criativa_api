import uuid

import pytest

from src.modules.get_member.app.get_member_usecase import GetMemberUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_GetMemberUsecase:
    def test_get_member(self):
        repo = MemberRepositoryMock()
        usecase = GetMemberUsecase(
            repo,
            observability=ObservabilityMock(module_name="get_member"),
        )

        member = usecase(member_id=str(repo.members[0].member_id))

        assert member == repo.members[0]

    def test_get_member_invalid_id(self):
        usecase = GetMemberUsecase(
            MemberRepositoryMock(),
            observability=ObservabilityMock(module_name="get_member"),
        )

        with pytest.raises(EntityError, match="Field member_id is not valid"):
            usecase(member_id="invalid")

    def test_get_member_wrong_id_type(self):
        usecase = GetMemberUsecase(
            MemberRepositoryMock(),
            observability=ObservabilityMock(module_name="get_member"),
        )

        with pytest.raises(EntityError, match="Field member_id is not valid"):
            usecase(member_id=123)

    def test_get_member_not_found(self):
        usecase = GetMemberUsecase(
            MemberRepositoryMock(),
            observability=ObservabilityMock(module_name="get_member"),
        )

        with pytest.raises(NoItemsFound, match="No items found for member_id"):
            usecase(member_id=str(uuid.uuid4()))
