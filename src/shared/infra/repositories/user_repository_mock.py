from typing import List, Optional
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(
                id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
                email="soller@soller.com",
                role=RoleEnum.USER,
                senha_hash="hash_fake_1"
            ),
            User(
                id=uuid.UUID("b9a52f40-0135-406d-b5d7-7ed5dce9bc8f"),
                email="brancas@brancas.com",
                role=RoleEnum.USER,
                senha_hash="hash_fake_2"
            ),
            User(
                id=uuid.UUID("c1a52f40-0135-406d-b5d7-7ed5dce9bc90"),
                email="bruno@bruno.com",
                role=RoleEnum.USER,
                senha_hash="hash_fake_3"
            )
        ]

    def get_user(self, user_id: uuid.UUID) -> User:
        for user in self.users:
            if str(user.id) == str(user_id):
                return user
        raise NoItemsFound("user_id")

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        return new_user

    def delete_user(self, user_id: uuid.UUID) -> User:
        for idx, user in enumerate(self.users):
            if str(user.id) == str(user_id):
                return self.users.pop(idx)
        raise NoItemsFound("user_id")

    def update_user(self, user: Optional[User] = None, **kwargs) -> User:
        if user is not None:
            for idx, u in enumerate(self.users):
                if u.id == user.id:
                    self.users[idx] = user
                    return user
            raise NoItemsFound("user_id")

        target_id = kwargs.get("user_id") or kwargs.get("id")
        for idx, u in enumerate(self.users):
            if str(u.id) == str(target_id):
                return u
        raise NoItemsFound("user_id")