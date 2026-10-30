import json

from src.modules.member.create_member.app import create_member_presenter
from src.shared.domain.enums.role_enum import RoleEnum


class Test_CreateMemberPresenter:
    def test_create_member_presenter(self, monkeypatch):
        admin_user = create_member_presenter.user_repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN}
        )
        monkeypatch.setattr(
            create_member_presenter.user_repo,
            "users",
            [admin_user, *create_member_presenter.user_repo.users[1:]],
        )
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": ["cookie1", "cookie2"],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "user": json.dumps({
                        "sub": str(admin_user.id),
                        "mail": "soller@soller.com",
                        "name": "Admin",
                    }),
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": '{"member_photo":"https://picsum.photos/800/600.jpg","member_name":"nome_membro","member_intro":"intro_membro"}',
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = create_member_presenter.lambda_handler(event, None)

        assert response["statusCode"] == 201

        body = json.loads(response["body"])
        assert str(body["member_photo"]) == "https://picsum.photos/800/600.jpg"
        assert body["member_name"] == "nome_membro"
        assert body["member_intro"] == "intro_membro"
        assert body["message"] == "the member was created successfully"
