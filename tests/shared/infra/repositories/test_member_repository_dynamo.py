import os
import pytest

#pytest.importorskip("src.shared.infra.repositories.member_repository_dynamo")

from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.member_repository_dynamo import MemberRepositoryDynamo
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_MemberRepositoryDynamo:

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_member(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()
        member_repository_mock = MemberRepositoryMock()
        member = member_repository_mock.members[0]
        resp = member_repository.create_member(member)

        assert resp.member_id == member.member_id
        assert resp.member_photo == member.member_photo
        assert resp.member_name == member.member_name
        assert resp.member_intro == member.member_intro


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_members(self):
        os.environ["STAGE"] = "TEST"

        member_repository = MemberRepositoryDynamo()

        resp = member_repository.get_all_members()

        assert len(resp) >= 3

