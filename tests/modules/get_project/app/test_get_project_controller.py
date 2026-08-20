from src.modules.get_project.app.get_project_controller import GetProjectController
from src.modules.get_project.app.get_project_usecase import GetProjectUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

import uuid

observability = ObservabilityMock(module_name="get_project")

class Test_GetProjectController:
    def test_get_project_controller(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo=repo, observability=observability)
        controller = GetProjectController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'project_id': str(repo.projects[1].id)
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['id'] == str(repo.projects[1].id)
        assert response.body['title'] == repo.projects[1].title
        assert response.body['description'] == repo.projects[1].description

    def test_get_project_controller_missing_parameters(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo=repo, observability=observability)
        controller = GetProjectController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field project_id is missing'


    def test_get_project_contoller_wrong_type_parameter(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo=repo, observability=observability)
        controller = GetProjectController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'project_id': 999
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field project_id isn't in the right type."

    def test_get_project_contoller_entity_error(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo=repo, observability=observability)
        controller = GetProjectController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'project_id': 'abc'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field project_id is not valid'

    def test_get_project_controller_no_items_found(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo=repo, observability=observability)
        controller = GetProjectController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={
            'project_id': str(uuid.uuid4())
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for project_id'
