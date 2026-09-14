from src.modules.get_all_projects.app.get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_GetAllProjectsUsecase:

    def test_get_all_projects_usecase(self):
        repo_mock = ProjectRepositoryMock()
        usecase = GetAllProjectsUsecase(repo_mock)

        all_projects_list_returned = usecase()

        assert all_projects_list_returned == repo_mock.projects
        assert len(all_projects_list_returned) == len(repo_mock.projects)
        
