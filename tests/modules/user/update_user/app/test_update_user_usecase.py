import pytest

from src.modules.user.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(selfs):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = UpdateUserUsecase(repo=repo)

        existing_user_id = str(repo.users[0].id)

        updated_user = usecase(
            user_id=existing_user_id,
            new_email="testeemail@devmaua.com.br",
            requester_user_id=repo.users[0].id,
        )

        assert updated_user.email == "testeemail@devmaua.com.br"

    def test_update_user_usecase_wrong_user_id(selfs):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(
                user_id="invalid-uuid",
                new_email="testeemail@devmaua.com.br",
                requester_user_id=repo.users[0].id,
            )

    def test_update_user_usecase_wrong_new_email(selfs):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = UpdateUserUsecase(repo=repo)

        existing_user_id = str(repo.users[0].id)

        with pytest.raises(EntityError):
            usecase(
                user_id=existing_user_id,
                new_email=1,
                requester_user_id=repo.users[0].id,
            )

    def test_update_user_usecase_forbidden_for_non_admin(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                user_id=str(repo.users[1].id),
                new_email="testeemail@devmaua.com.br",
                requester_user_id=repo.users[0].id,
            )

