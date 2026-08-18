from src.modules.delete_project.app.delete_project_controller import DeleteProjectController
from src.modules.delete_project.app.delete_project_usecase import DeleteProjectUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_DeleteprojectController:
    def test_delete_project_controller(self):
            repo = ProjectRepositoryMock()
            usecase = DeleteProjectUsecase(repo=repo)
            controller = DeleteProjectController(usecase=usecase)

            request = HttpRequest(body={
                'id': '1'
            })

            response = controller(request=request)

            assert response.status_code == 200
            assert response.body['message'] == 'the project was deleted successfully'

    def test_delete_project_controller_wrong_type(self):
            repo = ProjectRepositoryMock()
            usecase = DeleteProjectUsecase(repo=repo)
            controller = DeleteProjectController(usecase=usecase)

            request = HttpRequest(body={
                'id': 'a'
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'Field project_id is not valid'

    def test_delete_project_controller_missing_parameter(self):
            repo = ProjectRepositoryMock()
            usecase = DeleteProjectUsecase(repo=repo)
            controller = DeleteProjectController(usecase=usecase)

            request = HttpRequest(body={
                'id': '1'
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'Field project_id is missing'

    def test_delete_project_controller_invalid_project_id(self):
            repo = ProjectRepositoryMock()
            usecase = DeleteProjectUsecase(repo=repo)
            controller = DeleteProjectController(usecase=usecase)

            request = HttpRequest(body={
                'id': 2
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == "Field project_id isn't in the right type.\n Received: int.\n Expected: str"

    def test_delete_project_controller_no_items_found(self):
            repo = ProjectRepositoryMock()
            usecase = DeleteProjectUsecase(repo=repo)
            controller = DeleteProjectController(usecase=usecase)

            request = HttpRequest(body={
                'id': '69'
            })

            response = controller(request=request)

            assert response.status_code == 404
            assert response.body == 'No items found for project_id'
