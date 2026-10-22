import json

from src.modules.member.update_member.app import update_member_presenter as presenter_module
from src.modules.member.update_member.app.update_member_presenter import lambda_handler
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestUpdateMemberPresenter:
    def test_update_member(self):
        presenter_module.repo.members = MemberRepositoryMock().members
        target_member = presenter_module.repo.members[0]

        event = {
            "body": json.dumps(
                {
                    "member_id": str(target_member.member_id),
                    "new_member_name": "Updated Alice",
                }
            ),
            "headers": {},
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["member_id"] == str(target_member.member_id)
        assert body["member_photo"] == str(target_member.member_photo)
        assert body["member_name"] == "Updated Alice"
        assert body["member_intro"] == target_member.member_intro
        assert body["message"] == "the member was updated successfully"
