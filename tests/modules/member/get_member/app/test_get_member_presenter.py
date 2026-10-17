import json

from src.modules.get_member.app import get_member_presenter as presenter_module
from src.modules.get_member.app.get_member_presenter import lambda_handler


class Test_GetMemberPresenter:
    def test_get_member(self):
        member = presenter_module.repo.members[0]
        event = {
            "headers": {},
            "queryStringParameters": {"member_id": str(member.member_id)},
            "requestContext": {},
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["member_id"] == str(member.member_id)
        assert body["member_photo"] == str(member.member_photo)
        assert body["member_name"] == member.member_name
        assert body["member_intro"] == member.member_intro
        assert body["message"] == "the member was retrieved successfully"

    def test_get_member_not_found(self):
        event = {
            "headers": {},
            "queryStringParameters": {
                "member_id": "e1de4ef2-7d6c-4c4e-9ad2-a3ce22b0aeb1",
            },
            "requestContext": {},
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 404
        assert json.loads(response["body"]) == "No items found for member_id"
