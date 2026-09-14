from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

import uuid

class Test_DeleteUserController:
    def test_delete_user_controller(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUsecase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            existing_id =str(repo.users[0].id)

            request = HttpRequest(body={
                'user_id': existing_id
            })

            response = controller(request=request)

            assert response.status_code == 200
            assert response.body['message'] == 'the user was deleted successfully'

    def test_delete_user_controller_wrong_type(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUsecase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 'a'
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'Field user_id is not valid'

    def test_delete_user_controller_missing_parameter(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUsecase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'id': '1'
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == 'Field user_id is missing'

    def test_delete_user_controller_invalid_user_id(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUsecase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': 67
            })

            response = controller(request=request)

            assert response.status_code == 400
            assert response.body == "The field 'user_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_delete_user_controller_no_items_found(self):
            repo = UserRepositoryMock()
            usecase = DeleteUserUsecase(repo=repo)
            controller = DeleteUserController(usecase=usecase)

            request = HttpRequest(body={
                'user_id': str(uuid.uuid4())
            })

            response = controller(request=request)

            assert response.status_code == 404
            assert response.body == 'No items found for user_id'


