import pytest

from src.modules.project.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateProjectUsecase:
    def test_update_project(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)
        project = repo.projects[0]

        updated_project = usecase(
            project_id=project.id,
            new_title="Projeto atualizado",
            new_description="Descrição atualizada",
            requester_user_id=user_repo.users[0].id,
        )

        assert updated_project.id == project.id
        assert updated_project.title == "Projeto atualizado"
        assert updated_project.description == "Descrição atualizada"
        assert repo.projects[0] == updated_project

    def test_update_project_forbidden_for_non_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                project_id=repo.projects[0].id,
                new_title="Projeto atualizado",
                new_description="Descrição atualizada",
                requester_user_id=user_repo.users[0].id,
            )
