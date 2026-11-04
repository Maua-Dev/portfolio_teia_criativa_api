import uuid

from src.modules.user.auth_user.app.auth_user_controller import AuthUserController
from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserController:

    def _controller(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUsecase(user_repo=repo)
        return AuthUserController(usecase=usecase), repo

    def test_auth_user_controller_retrieves_existing_user(self):
        controller, repo = self._controller()
        existing = repo.users[0]

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(existing.id),
                "name": existing.user_name,
                "mail": existing.email,
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["id"] == str(existing.id)
        assert response.body["email"] == existing.email
        assert response.body["user_name"] == existing.user_name
        assert response.body["role"] == existing.role.value
        assert response.body["active"] is True
        assert response.body["message"] == "the user was retrieved successfully"

    def test_auth_user_controller_creates_new_user(self):
        controller, repo = self._controller()
        new_id = str(uuid.UUID("d2a52f40-0135-406d-b5d7-7ed5dce9bc91"))

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": new_id,
                "name": "Novo Usuario",
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body["id"] == new_id
        assert response.body["email"] == "21.00000-0@maua.br"
        assert response.body["user_name"] == "Novo Usuario"
        assert response.body["role"] == "User"
        assert response.body["active"] is True
        assert response.body["message"] == "the user was created successfully"
        assert len(repo.users) == 4

    def test_auth_user_controller_missing_user_from_authorizer(self):
        controller, _ = self._controller()

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == f"Field {USER_FROM_AUTHORIZER_KEY} is missing"

    def test_auth_user_controller_missing_sub(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "name": "Nome",
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field sub is missing"

    def test_auth_user_controller_missing_name(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is missing"

    def test_auth_user_controller_missing_mail(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(uuid.uuid4()),
                "name": "Nome",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field mail is missing"

    def test_auth_user_controller_wrong_type_sub(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": 123,
                "name": "Nome",
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "sub" in response.body

    def test_auth_user_controller_wrong_type_name(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(uuid.uuid4()),
                "name": 123,
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "name" in response.body

    def test_auth_user_controller_wrong_type_mail(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(uuid.uuid4()),
                "name": "Nome",
                "mail": 123,
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "mail" in response.body

    def test_auth_user_controller_invalid_uuid_sub(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": "not-a-uuid",
                "name": "Nome",
                "mail": "21.00000-0@maua.br",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is not valid"

    def test_auth_user_controller_invalid_email(self):
        controller, _ = self._controller()

        request = HttpRequest(body={
            USER_FROM_AUTHORIZER_KEY: {
                "sub": str(uuid.uuid4()),
                "name": "Nome",
                "mail": "email_invalido",
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "email" in response.body
