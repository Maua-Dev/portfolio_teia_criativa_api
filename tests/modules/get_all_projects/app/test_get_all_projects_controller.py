from src.modules.get_all_projects.app.get_all_projects_controller import GetAllProjectsController
from src.modules.get_all_projects.app.get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_GetAllProjectsController:

    def test_get_all_projects_controller(self):
        repo_mock = ProjectRepositoryMock()
        get_all_projects_usecase = GetAllProjectsUsecase(repo_mock)
        controller = GetAllProjectsController(get_all_projects_usecase)

        response = controller(None)

        assert response.status_code == 200