import os
import pytest

pytest.importorskip("src.shared.infra.repositories.user_repository_dynamo")

from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryDynamo:

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        user = user_repository_mock.users[0]
        resp = user_repository.create_user(user)

        assert resp.id == user.id
        assert resp.email == user.email
        assert resp.role == user.role
        assert resp.active == user.active
        assert resp.user_name == user.user_name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user_duplicated(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user = UserRepositoryMock().users[0]
        user_repository.create_user(user)

        with pytest.raises(DuplicatedItem):
            user_repository.create_user(user)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user = UserRepositoryMock().users[0]

        resp = user_repository.get_user(user.id)

        assert resp.id == user.id
        assert resp.email == user.email
        assert resp.role == user.role
        assert resp.active == user.active
        assert resp.user_name == user.user_name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()

        resp = user_repository.get_all_user()

        assert len(resp) >= 3

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user = UserRepositoryMock().users[0]

        updated = user.model_copy(update={"user_name": "username_updated"})
        resp = user_repository.update_user(updated)

        assert resp.user_name == "username_updated"
        assert user_repository.get_user(user.id).user_name == "username_updated"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user = UserRepositoryMock().users[2]

        resp = user_repository.delete_user(user.id)

        assert resp.id == user.id
        with pytest.raises(NoItemsFound):
            user_repository.get_user(user.id)