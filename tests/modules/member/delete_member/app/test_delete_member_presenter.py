import json

from src.modules.member.delete_member.app import delete_member_presenter as presenter_module
from src.modules.member.delete_member.app.delete_member_presenter import lambda_handler
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestDeleteMemberPresenter:
    def test_delete_member(self):
        presenter_module.repo.members = MemberRepositoryMock().members
        target_member = presenter_module.repo.members[0]

        event = {
            "body": json.dumps({"member_id": str(target_member.member_id)}),
            "headers": {},
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == {
            "member_id": str(target_member.member_id),
            "member_photo": str(target_member.member_photo),
            "member_name": target_member.member_name,
            "member_intro": target_member.member_intro,
            "message": "the member was deleted successfully",
        }
