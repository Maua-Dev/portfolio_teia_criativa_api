import uuid

import pytest

from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserUsecase:

    def test_auth_user_usecase_retrieves_existing_user(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo=repo)
        existing = repo.users[0]

        user, case_number = usecase(
            user_id=existing.id,
            user_name="ignored_name",
            user_email="ignored@maua.br",
        )

        assert case_number == 0
        assert user.id == existing.id
        assert user.email == existing.email
        assert user.user_name == existing.user_name
        assert len(repo.users) == 3

    def test_auth_user_usecase_creates_new_user(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo=repo)
        new_id = uuid.UUID("d2a52f40-0135-406d-b5d7-7ed5dce9bc91")

        user, case_number = usecase(
            user_id=new_id,
            user_name="Novo Usuario",
            user_email="21.00000-0@maua.br",
        )

        assert case_number == 1
        assert user.id == new_id
        assert user.email == "21.00000-0@maua.br"
        assert user.user_name == "Novo Usuario"
        assert user.role == RoleEnum.USER
        assert user.active is True
        assert len(repo.users) == 4

    def test_auth_user_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo=repo)

        with pytest.raises(EntityError):
            usecase(
                user_id=uuid.uuid4(),
                user_name="Nome",
                user_email="email_invalido_sem_arroba",
            )
