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

        updated_user = self.repo.update_user(user_id=user_id, new_email=new_email)

        return updated_user
