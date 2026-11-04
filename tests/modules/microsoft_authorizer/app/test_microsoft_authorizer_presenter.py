import json
import uuid

from src.modules.microsoft_authorizer.app import microsoft_authorizer_presenter as presenter_module
from src.modules.microsoft_authorizer.app.microsoft_authorizer_presenter import lambda_handler
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class _FakeGraphClient:
    def __init__(self, profile: dict | None = None, error: Exception | None = None):
        self.profile = profile or {}
        self.error = error

    def get_user_profile(self, access_token: str) -> dict:
        if self.error is not None:
            raise self.error
        return self.profile


class Test_MicrosoftAuthorizerPresenter:

    def test_presenter_allows_existing_user(self):
        user_id = uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        presenter_module.user_repo.users[0] = User(
            id=user_id,
            email="21.00000-0@maua.br",
            role=RoleEnum.USER,
            user_name="Soller",
        )
        presenter_module.usecase.graph_client = _FakeGraphClient(
            profile={
                "id": str(user_id),
                "mail": "21.00000-0@maua.br",
                "displayName": "Soller",
            }
        )

        response = lambda_handler(
            {
                "authorizationToken": "Bearer token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/GET/users",
            },
            None,
        )

        assert response["principalId"] == str(user_id)
        assert response["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(response["context"]["user"])["mail"] == "21.00000-0@maua.br"

    def test_presenter_denies_when_graph_fails(self):
        presenter_module.usecase.graph_client = _FakeGraphClient(
            error=Exception("graph down")
        )

        response = lambda_handler(
            {
                "authorizationToken": "Bearer token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/GET/users",
            },
            None,
        )

        assert response["policyDocument"]["Statement"][0]["Effect"] == "Deny"
        assert response["principalId"] == "user"

    def test_presenter_allows_onboarding_route(self):
        new_id = str(uuid.uuid4())
        presenter_module.usecase.graph_client = _FakeGraphClient(
            profile={
                "id": new_id,
                "mail": "21.99999-9@maua.br",
                "displayName": "Novo User",
            }
        )

        response = lambda_handler(
            {
                "authorizationToken": "token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/POST/auth",
            },
            None,
        )

        assert response["principalId"] == new_id
        assert response["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(response["context"]["user"])["name"] == "Novo User"
