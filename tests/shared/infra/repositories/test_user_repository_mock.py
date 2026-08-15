import pytest
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"))

        assert user.email == "soller@soller.com"
        assert user.id == uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        assert user.role == RoleEnum.USER

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_user(uuid.uuid4())

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()
        assert len(users) == 3

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            id=uuid.UUID("d2a52f40-0135-406d-b5d7-7ed5dce9bc91"),
            email="dohype@vitin.com",
            senha_hash="hash_fake_4",
            role=RoleEnum.USER
        )

        repo.create_user(user)

        assert repo.users[3].email == "dohype@vitin.com"
        assert repo.users[3].id == uuid.UUID("d2a52f40-0135-406d-b5d7-7ed5dce9bc91")

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user(uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"))
        assert user.email == "soller@soller.com"

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_user(uuid.uuid4())

    def test_update_user(self):
        repo = UserRepositoryMock()
        updated = User(
            id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
            email="novo_email@soller.com",
            senha_hash="hash_fake_1",
            role=RoleEnum.USER
        )
        user = repo.update_user(updated)
        assert user.email == "novo_email@soller.com"
        assert repo.users[0].email == "novo_email@soller.com"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        non_existent_user = User(
            id=uuid.uuid4(),
            email="yurialberto@yurialberto.com",
            senha_hash="hash_fake_x",
            role=RoleEnum.USER
        )
        with pytest.raises(NoItemsFound):
            repo.update_user(non_existent_user)
