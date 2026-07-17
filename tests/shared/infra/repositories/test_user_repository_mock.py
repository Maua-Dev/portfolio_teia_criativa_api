from uuid import uuid4

from src.shared.domain.entities.user import RoleEnum, User
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        expected_user = repo.users[0]

        user = repo.get_user(expected_user.id)

        assert user.email == "soller@soller.com"
        assert user.id == expected_user.id
        assert user.role == RoleEnum.ADMIN
        assert user.senha_hash == "hash_fake_1"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            user = repo.get_user(uuid4())

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 3

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            email="dohype@vitin.com",
            id=uuid4(),
            role=RoleEnum.USER,
            senha_hash="hash_fake_4"
        )

        repo.create_user(user)

        assert repo.get_user_counter() == 4

    def test_delete_user(self):
        repo = UserRepositoryMock()
        target_id = repo.users[0].id

        deleted_user = repo.delete_user(target_id)

        assert deleted_user.email == "soller@soller.com"
        assert deleted_user.id == target_id
        assert deleted_user.role == RoleEnum.ADMIN
        assert deleted_user.senha_hash == "hash_fake_1"
        assert repo.get_user_counter() == 2

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
           repo.delete_user(uuid4())

    def test_update_user(self):
        repo = UserRepositoryMock()
        target_id = repo.users[0].id
        updated_user = User(
            email="soller@soller.com",
            id=target_id,
            role=RoleEnum.USER,
            senha_hash="hash_fake_novo"
        )

        user = repo.update_user(updated_user)

        assert user.role == RoleEnum.USER
        assert user.senha_hash == "hash_fake_novo"
        assert repo.users[0].role == RoleEnum.USER
        assert repo.users[0].senha_hash == "hash_fake_novo"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        non_existent_user = User(
            email="yurialberto@yurialberto.com",
            id=uuid4(),
            role=RoleEnum.USER,
            senha_hash="hash_fake_x"
        )
        with pytest.raises(NoItemsFound):
            user = repo.update_user(non_existent_user)

    def test_get_users_counter(self):
        repo = UserRepositoryMock()

        assert repo.get_user_counter() == 3

