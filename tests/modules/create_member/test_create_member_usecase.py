import pytest
from pydantic import HttpUrl

from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateMemberUsecase:
    def test_create_member_usecase(self):
        repo = MemberRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateMemberUsecase(repo=repo, user_repo=user_repo)

        member = usecase(
            member_photo='https://picsum.photos/800/600.jpg',
            member_name='nome_membro',
            member_intro='intro_membro',
            requester_id=str(user_repo.users[0].id)
        )

        assert member.member_photo == HttpUrl('https://picsum.photos/800/600.jpg')
        assert member.member_name == 'nome_membro'
        assert member.member_intro == 'intro_membro'
        assert member in repo.members

    def test_create_member_usecase_invalid_photo_extension(self):
        repo = MemberRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateMemberUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(ValueError):
            usecase(
                member_photo='https://picsum.photos/800/600.bmp',
                member_name='nome_membro',
                member_intro='intro_membro',
                requester_id=str(user_repo.users[0].id)
            )

    def test_create_member_usecase_rejects_non_admin(self):
        repo = MemberRepositoryMock()
        user_repo = UserRepositoryMock()
        original_members = repo.members.copy()
        usecase = CreateMemberUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                member_photo='https://picsum.photos/800/600.jpg',
                member_name='nome_membro',
                member_intro='intro_membro',
                requester_id=str(user_repo.users[0].id)
            )

        assert repo.members == original_members

    def test_create_member_usecase_invalid_requester_id(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo, user_repo=UserRepositoryMock())

        with pytest.raises(EntityError):
            usecase(
                member_photo='https://picsum.photos/800/600.jpg',
                member_name='nome_membro',
                member_intro='intro_membro',
                requester_id='invalid-uuid'
            )
