from src.modules.project.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_CreateProjectUsecase:
    def test_create_project(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        project = usecase(
            title="Novo projeto",
            description="Projeto criado no teste",
            associates=None,
            display_image=None,
        )

        assert repo.projects[-1] == project
        assert project.title == "Novo projeto"
        assert project.description == "Projeto criado no teste"
