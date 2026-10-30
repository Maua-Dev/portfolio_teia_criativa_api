import uuid

import pytest

from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def create_repositories(role=RoleEnum.ADMIN, active=True):
    member_repo = MemberRepositoryMock()
    user_repo = UserRepositoryMock()
    user_repo.users[0] = user_repo.users[0].model_copy(
        update={"role": role, "active": active}
    )
    return member_repo, user_repo


class TestDeleteMemberUsecase:
    def test_delete_member(self):
        member_repo, user_repo = create_repositories()
        member = member_repo.members[0]

        deleted_member = DeleteMemberUsecase(member_repo, user_repo)(
            str(member.member_id), str(user_repo.users[0].id)
        )

        assert deleted_member == member
        assert member not in member_repo.members

    def test_delete_member_rejects_non_admin(self):
        member_repo, user_repo = create_repositories(role=RoleEnum.USER)
        member = member_repo.members[0]

        with pytest.raises(ForbiddenAction):
            DeleteMemberUsecase(member_repo, user_repo)(
                str(member.member_id), str(user_repo.users[0].id)
            )

        assert member in member_repo.members

    def test_delete_member_rejects_inactive_admin(self):
        member_repo, user_repo = create_repositories(active=False)
        member = member_repo.members[0]

        with pytest.raises(ForbiddenAction):
            DeleteMemberUsecase(member_repo, user_repo)(
                str(member.member_id), str(user_repo.users[0].id)
            )

        assert member in member_repo.members

    @pytest.mark.parametrize("requester_id", [None, "invalid-uuid", 123])
    def test_delete_member_rejects_invalid_requester_id(self, requester_id):
        member_repo, user_repo = create_repositories()

        with pytest.raises(EntityError, match="Field requester_id is not valid"):
            DeleteMemberUsecase(member_repo, user_repo)(
                str(member_repo.members[0].member_id), requester_id
            )

    @pytest.mark.parametrize("member_id", [None, "not-a-uuid", 123])
    def test_delete_member_rejects_invalid_member_id(self, member_id):
        member_repo, user_repo = create_repositories()

        with pytest.raises(EntityError, match="Field member_id is not valid"):
            DeleteMemberUsecase(member_repo, user_repo)(
                member_id, str(user_repo.users[0].id)
            )

    def test_delete_member_not_found(self):
        member_repo, user_repo = create_repositories()

        with pytest.raises(NoItemsFound):
            DeleteMemberUsecase(member_repo, user_repo)(
                str(uuid.uuid4()), str(user_repo.users[0].id)
            )
