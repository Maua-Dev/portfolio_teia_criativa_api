import json

from src.modules.get_all_members.app.get_all_members_presenter import lambda_handler
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestGetAllMembersPresenter:
    def test_returns_all_members_in_http_response(self):
        response = lambda_handler(event={}, context=None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == {
            "all_members": [
                {
                    "member_id": str(member.member_id),
                    "member_photo": str(member.member_photo),
                    "member_name": member.member_name,
                    "member_intro": member.member_intro,
                }
                for member in MemberRepositoryMock().get_all_members()
            ],
            "message": "all members has been retrieved",
        }
