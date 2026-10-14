import pytest
from pydantic import HttpUrl

from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_CreateMemberUsecase:
    def test_create_member_usecase(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)

        member = usecase(
            member_photo='https://picsum.photos/800/600.jpg',
            member_name='nome_membro',
            member_intro='intro_membro'
        )

        assert member.member_photo == HttpUrl('https://picsum.photos/800/600.jpg')
        assert member.member_name == 'nome_membro'
        assert member.member_intro == 'intro_membro'
        assert member in repo.members

    def test_create_member_usecase_invalid_photo_extension(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)

        with pytest.raises(ValueError):
            usecase(
                member_photo='https://picsum.photos/800/600.png',
                member_name='nome_membro',
                member_intro='intro_membro'
            )
