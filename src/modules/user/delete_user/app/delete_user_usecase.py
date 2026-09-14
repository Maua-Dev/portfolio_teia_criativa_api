from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

import uuid


class DeleteUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> User:

        try:
            parsed_id = uuid.UUID(user_id)
        except ValueError:
            raise EntityError("user_id")

        user = self.repo.delete_user(parsed_id)

        if user is None:
            raise NoItemsFound("user_id")

        return user
