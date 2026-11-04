import json

from src.modules.project.create_project.app import create_project_presenter as presenter_module
from src.modules.project.create_project.app.create_project_presenter import lambda_handler
from src.shared.domain.enums.role_enum import RoleEnum


class Test_CreateProjectPresenter:
    def test_create_project(self):
        admin = presenter_module.user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        presenter_module.user_repo.users[0] = admin

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {
                "header1": "value1"
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authorizer": {
                    "user": json.dumps({
                        "sub": str(admin.id),
                        "mail": admin.email,
                        "name": admin.user_name,
                    })
                },
                "http": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
            },
            "body": '{"title":"Novo projeto", "description":"Projeto criado no teste"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        assert json.loads(response["body"])["message"] == "the project was created successfully"
