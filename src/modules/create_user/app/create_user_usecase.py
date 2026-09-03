import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, role: RoleEnum = RoleEnum.USER, active=True, user_name=str) -> User:
        user = User(
            id=uuid.uuid4(),
            email=email,
            role=role,
            active=active,
            user_name=user_name
        )

        return self.repo.create_user(user)