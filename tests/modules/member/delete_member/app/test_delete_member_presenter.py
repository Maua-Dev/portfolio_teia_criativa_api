import json

from src.modules.member.delete_member.app import delete_member_presenter
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestDeleteMemberPresenter:
    def test_delete_member_presenter(self, monkeypatch):
        admin_user = delete_member_presenter.user_repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN}
        )
        monkeypatch.setattr(delete_member_presenter.user_repo, "users", [admin_user])
        monkeypatch.setattr(
            delete_member_presenter.repo,
            "members",
            MemberRepositoryMock().members,
        )
        member = delete_member_presenter.repo.members[0]
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/members",
            "headers": {},
            "requestContext": {
                "authorizer": {
                    "user": json.dumps(
                        {
                            "sub": str(admin_user.id),
                            "mail": str(admin_user.email),
                            "name": admin_user.user_name,
                        }
                    )
                }
            },
            "body": json.dumps({"member_id": str(member.member_id)}),
        }

        response = delete_member_presenter.lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": member.member_name,
            "member_intro": member.member_intro,
            "message": "the member was deleted successfully",
        }

    def test_delete_member_presenter_rejects_identity_from_request_body(self):
        member = delete_member_presenter.repo.members[0]
        event = {
            "headers": {},
            "body": json.dumps(
                {
                    "member_id": str(member.member_id),
                    "user_from_authorizer": {
                        "sub": str(delete_member_presenter.user_repo.users[0].id)
                    },
                }
            ),
        }

        response = delete_member_presenter.lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Field requester_id is not valid"
        assert member in delete_member_presenter.repo.members
