import json
import uuid

from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import (
    MicrosoftAuthorizerUsecase,
)
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class _FakeGraphClient:
    def __init__(self, profile: dict | None = None, error: Exception | None = None):
        self.profile = profile or {}
        self.error = error
        self.last_token = None

    def get_user_profile(self, access_token: str) -> dict:
        self.last_token = access_token
        if self.error is not None:
            raise self.error
        return self.profile


class Test_MicrosoftAuthorizerUsecase:

    def _usecase(self, profile: dict, repo: UserRepositoryMock | None = None):
        repo = repo or UserRepositoryMock()
        return MicrosoftAuthorizerUsecase(
            graph_client=_FakeGraphClient(profile=profile),
            user_repo=repo,
        ), repo

    def test_allow_existing_user_on_protected_route(self):
        user_id = uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        repo = UserRepositoryMock()
        repo.users[0] = User(
            id=user_id,
            email="21.00000-0@maua.br",
            role=RoleEnum.USER,
            user_name="Soller",
        )
        usecase, _ = self._usecase(
            {
                "id": str(user_id),
                "mail": "21.00000-0@maua.br",
                "displayName": "Soller",
            },
            repo=repo,
        )

        policy = usecase(
            authorization_token="Bearer token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["principalId"] == str(user_id)
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        context_user = json.loads(policy["context"]["user"])
        assert context_user == {
            "sub": str(user_id),
            "mail": "21.00000-0@maua.br",
            "name": "Soller",
        }

    def test_deny_when_user_missing_on_protected_route(self):
        usecase, _ = self._usecase(
            {
                "id": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
                "displayName": "Novo",
            }
        )

        policy = usecase(
            authorization_token="token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"
        assert "context" not in policy

    def test_allow_onboarding_route_without_existing_user(self):
        user_id = str(uuid.uuid4())
        usecase, _ = self._usecase(
            {
                "id": user_id,
                "mail": "21.00000-0@maua.br",
                "displayName": "Novo",
            }
        )

        policy = usecase(
            authorization_token="Bearer token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["principalId"] == user_id
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        context_user = json.loads(policy["context"]["user"])
        assert context_user["mail"] == "21.00000-0@maua.br"
        assert context_user["name"] == "Novo"

    def test_deny_non_maua_email(self):
        usecase, _ = self._usecase(
            {
                "id": str(uuid.uuid4()),
                "mail": "user@gmail.com",
                "displayName": "External",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_invalid_uuid_sub(self):
        usecase, _ = self._usecase(
            {
                "id": "not-a-uuid",
                "mail": "21.00000-0@maua.br",
                "displayName": "Nome",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_uses_user_principal_name_when_mail_missing(self):
        user_id = uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        repo = UserRepositoryMock()
        repo.users[0] = User(
            id=user_id,
            email="21.00000-0@maua.br",
            role=RoleEnum.USER,
            user_name="Soller",
        )
        usecase, _ = self._usecase(
            {
                "id": str(user_id),
                "userPrincipalName": "21.00000-0@maua.br",
                "displayName": "Soller",
            },
            repo=repo,
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(policy["context"]["user"])["mail"] == "21.00000-0@maua.br"

    def test_strips_bearer_prefix_before_graph_call(self):
        graph = _FakeGraphClient(
            profile={
                "id": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
                "displayName": "Novo",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(
            graph_client=graph,
            user_repo=UserRepositoryMock(),
        )

        usecase(
            authorization_token="Bearer abc.def",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert graph.last_token == "abc.def"
