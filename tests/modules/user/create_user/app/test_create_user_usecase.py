import pytest

from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.role_enum import RoleEnum

class Test_CreateUserUsecase:

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateUserUsecase(repo=repo)

        user = usecase(
            email="novo_user@teste.com",
            user_name="user_name_test1",
            requester_user_id=repo.users[0].id,
        )

        assert user.email == "novo_user@teste.com"
        assert user.role == RoleEnum.USER
        assert user.user_name == "user_name_test1"

    def test_create_user_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(
                email="email_invalido_sem_arroba",
                user_name="user_name_test1",
                requester_user_id=repo.users[0].id,
            )

    def test_create_user_usecase_forbidden_for_non_admin(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                email="novo_user@teste.com",
                user_name="user_name_test1",
                requester_user_id=repo.users[0].id,
            )

    def test_create_user_usecase_forbidden_for_inactive_admin(self):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = CreateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                email="novo_user@teste.com",
                user_name="user_name_test1",
                requester_user_id=repo.users[0].id,
            )

