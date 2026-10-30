import json
import uuid

from src.modules.user.auth_user.app import auth_user_presenter as presenter_module
from src.modules.user.auth_user.app.auth_user_presenter import lambda_handler


class Test_AuthUserPresenter:

    def _event(self, *, sub: str, name: str, mail: str):
        return {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/auth",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "sub": sub,
                        "name": name,
                        "mail": mail,
                    })
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
                    "method": "POST",
                    "path": "/auth",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent",
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390,
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
        }

    def test_auth_user_presenter_retrieves_existing_user(self):
        existing = presenter_module.user_repo.users[0]

        response = lambda_handler(
            self._event(
                sub=str(existing.id),
                name=existing.user_name,
                mail=existing.email,
            ),
            None,
        )

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["id"] == str(existing.id)
        assert body["email"] == existing.email
        assert body["user_name"] == existing.user_name
        assert body["message"] == "the user was retrieved successfully"

    def test_auth_user_presenter_creates_new_user(self):
        new_id = str(uuid.UUID("e3a52f40-0135-406d-b5d7-7ed5dce9bc92"))
        initial_count = len(presenter_module.user_repo.users)

        response = lambda_handler(
            self._event(
                sub=new_id,
                name="Presenter User",
                mail="21.99999-9@maua.br",
            ),
            None,
        )

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert body["id"] == new_id
        assert body["email"] == "21.99999-9@maua.br"
        assert body["user_name"] == "Presenter User"
        assert body["message"] == "the user was created successfully"
        assert len(presenter_module.user_repo.users) == initial_count + 1

    def test_auth_user_presenter_missing_authorizer_user(self):
        event = self._event(
            sub=str(uuid.uuid4()),
            name="Nome",
            mail="21.00000-0@maua.br",
        )
        event["requestContext"]["authorizer"] = {}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "user_from_authorizer" in body
