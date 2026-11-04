from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.auth.authorization import require_admin
from src.shared.helpers.errors.domain_errors import EntityError
import uuid

class UpdateProjectUsecase:
    def __init__(self, repo: IProjectRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self, project_id: uuid.UUID, new_title: str, new_description: str, requester_user_id: uuid.UUID) -> Project:

        require_admin(self.user_repo, requester_user_id)

        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")
        
        if type(new_title) != str:
            raise EntityError("new_title")

        if type(new_description) != str:
            raise EntityError('new_description')

        current_project = self.repo.get_project(project_id)
        updated_project = Project(
            id=current_project.id,
            title=new_title,
            description=new_description,
            associates=current_project.associates,
            display_image=current_project.display_image,
        )

        return self.repo.update_project(updated_project)
