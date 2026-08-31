from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError

import uuid

class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, new_email: str) -> User:

        try:
            uuid.UUID(user_id)
        except ValueError:
            raise EntityError("user_id")

        if type(new_email) != str:
            raise EntityError("new_email")

        user = self.repo.get_user(user_id=uuid.UUID(user_id))

        updated_user = User(
            id=user.id,
            email=new_email,
            role=user.role,
            senha_hash=user.senha_hash
        )

        return self.repo.update_user(user=updated_user)