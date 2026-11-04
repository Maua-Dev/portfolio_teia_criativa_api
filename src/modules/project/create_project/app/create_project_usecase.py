from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.auth.authorization import require_admin
import uuid
from typing import Optional

class CreateProjectUsecase:
    def __init__(self, repo: IProjectRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self, title: str, description: str, associates: Optional[list[uuid.UUID]], display_image: Optional[str], requester_user_id: uuid.UUID) -> Project:

        require_admin(self.user_repo, requester_user_id)

        project = Project(
            title=title,
            description=description,
            associates=associates,
            display_image=display_image
        )

        return self.repo.create_project(project)
