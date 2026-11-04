import pytest

from src.modules.project.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateProjectUsecase:
    def test_create_project(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateProjectUsecase(repo, user_repo)

        project = usecase(
            title="Novo projeto",
            description="Projeto criado no teste",
            associates=None,
            display_image=None,
            requester_user_id=user_repo.users[0].id,
        )

        assert repo.projects[-1] == project
        assert project.title == "Novo projeto"
        assert project.description == "Projeto criado no teste"

    def test_create_project_forbidden_for_non_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateProjectUsecase(repo, user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                title="Novo projeto",
                description="Projeto criado no teste",
                associates=None,
                display_image=None,
                requester_user_id=user_repo.users[0].id,
            )

    def test_create_project_forbidden_for_inactive_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = CreateProjectUsecase(repo, user_repo)

        with pytest.raises(ForbiddenAction):
            usecase(
                title="Novo projeto",
                description="Projeto criado no teste",
                associates=None,
                display_image=None,
                requester_user_id=user_repo.users[0].id,
            )
