from typing import List

from src.shared.domain.entities.user import RoleEnum, User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from uuid import UUID, uuid4


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(email="soller@soller.com", id=str(uuid4())
                 , role=RoleEnum.ADMIN, senha_hash ="hash_fake_1"),
            User(email="brancas@brancas.com", id=str(uuid4()), role=RoleEnum.USER, senha_hash ="hash_fake_2"),
            User(email="bruno@bruno.com", id=str(uuid4()), role=RoleEnum.ADMIN, senha_hash ="hash_fake_3")
        ]

    def get_user(self, id: str) -> User:
        for user in self.users:
            if str(user.id) == str(id):
                return user
        return None

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        self.users.append(new_user)
        return new_user

    def delete_user(self, id: str) -> User:
        for idx, user in enumerate(self.users):
            if str(user.id) == str(id):
                return self.users.pop(idx)

        return None
    
    def update_user(self, user: User) -> User:
        for idx, existing_user in enumerate(self.users):
            if str(existing_user.id) == str(user.id):
                self.users[idx] = user
                return user
        return None
