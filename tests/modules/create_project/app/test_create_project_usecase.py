import pytest
import uuid
from src.modules.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_CreateProjectUsecase:

    def test_create_user(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)
            
        project = usecase(
            title="Teia Criativa",
            description="Descrição do projeto",
            associates=None,
            display_image=None,
        )

        assert repo.projects[-1] == project

    def test_create_project_with_all_field(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        project = usecase(
            title="Vitor Choueri",
            description="branco@branco.branco",
            associates=[uuid.uuid4(), uuid.uuid4()],
            display_image="https://exemplo.com/imagem.png"
        )

        assert repo.projects[-1] == project

    def test_create_project_with_invalid_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(EntityError):
            project = usecase(
                title="D",
                description="Descrição do projeto Dev Bank",
                associates=None,
                display_image=None,
            )

    def test_create_user_invalid_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(EntityError):
            project = usecase(
                title="Dev Bank",
                description="D",
                associates=None,
                display_image=None,
            )

    def test_create_project_usecase_missing_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase()

        with pytest.raises(EntityError):
            project = usecase(
                title=None,
                description="Projeto da dev",
                associates=None,
                display_image=None
            )

    def test_crate_project_usecase_missing_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase()

        with pytest.raises(EntityError):
            project = usecase(
                title="Dev Médias",
                description=None,
                associates=None,
                display_image=None
            )
