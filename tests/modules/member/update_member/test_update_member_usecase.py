import pytest

from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def test_update_member_usecase():
    member_repo = MemberRepositoryMock()
    user_repo = UserRepositoryMock()
    admin = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    user_repo.users[0] = admin
    usecase = UpdateMemberUsecase(member_repo, user_repo)

    updated = usecase(
        member_id=str(member_repo.members[0].member_id),
        member_photo="https://picsum.photos/800/600.jpg",
        member_name="updated_name",
        member_intro="updated_intro",
        requester_id=str(admin.id),
    )

    assert updated.member_name == "updated_name"
    assert updated.member_intro == "updated_intro"
    assert member_repo.members[0] == updated


def test_update_member_usecase_rejects_non_admin():
    member_repo = MemberRepositoryMock()
    usecase = UpdateMemberUsecase(member_repo, UserRepositoryMock())
    original_members = member_repo.members.copy()

    with pytest.raises(ForbiddenAction):
        usecase(
            member_id=str(member_repo.members[0].member_id),
            member_photo="https://picsum.photos/800/600.jpg",
            member_name="updated_name",
            member_intro="updated_intro",
            requester_id="af852f40-0135-406d-b5d7-7ed5dce9bc8e",
        )

    assert member_repo.members == original_members


def test_update_member_usecase_rejects_inactive_admin():
    member_repo = MemberRepositoryMock()
    user_repo = UserRepositoryMock()
    inactive_admin = user_repo.users[0].model_copy(
        update={"role": RoleEnum.ADMIN, "active": False}
    )
    user_repo.users[0] = inactive_admin
    usecase = UpdateMemberUsecase(member_repo, user_repo)

    with pytest.raises(ForbiddenAction):
        usecase(
            member_id=str(member_repo.members[0].member_id),
            member_photo="https://picsum.photos/800/600.jpg",
            member_name="updated_name",
            member_intro="updated_intro",
            requester_id=str(inactive_admin.id),
        )


def test_update_member_usecase_rejects_invalid_requester_id():
    usecase = UpdateMemberUsecase(MemberRepositoryMock(), UserRepositoryMock())

    with pytest.raises(EntityError):
        usecase(
            member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
            member_photo="https://picsum.photos/800/600.jpg",
            member_name="updated_name",
            member_intro="updated_intro",
            requester_id="invalid-uuid",
        )
