import pytest

from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        existing_user_id = str(repo.users[0].id)

        updated_user = usecase(user_id=existing_user_id, new_email="testeemail@devmaua.com.br")

        assert updated_user.email == "testeemail@devmaua.com.br"

    def test_update_user_usecase_wrong_user_id(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="invalid-uuid", new_email="testeemail@devmaua.com.br")

    def test_update_user_usecase_wrong_new_email(selfs):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        existing_user_id = str(repo.users[0].id)

        with pytest.raises(EntityError):
            usecase(user_id=existing_user_id, new_email=1)

