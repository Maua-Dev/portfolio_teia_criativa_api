import pytest

from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.role_enum import RoleEnum

class Test_CreateUserUsecase:

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)

        user = usecase(email="novo_user@teste.com", senha_hash="senha_hash_123")

        assert user.email == "novo_user@teste.com"
        assert user.role == RoleEnum.USER
        assert user.senha_hash == "senha_hash_123"

    def test_create_user_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(email="email_invalido_sem_arroba", senha_hash="hash_senha_123")


