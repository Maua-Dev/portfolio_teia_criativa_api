from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, senha_hash: str, role: RoleEnum = RoleEnum.USER) -> User:
        try:
            user = User(
                email=email,
                senha_hash=senha_hash,
                role=role,
            )
        except Exception:
            raise EntityError('User')
       
        return self.repo.create_user(user)
