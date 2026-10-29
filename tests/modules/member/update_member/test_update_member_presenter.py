import json


from src.modules.member.update_member.app import update_member_presenter
from src.shared.domain.enums.role_enum import RoleEnum


def test_update_member_presenter(monkeypatch):
    admin = update_member_presenter.user_repo.users[0].model_copy(
        update={"role": RoleEnum.ADMIN}
    )
    monkeypatch.setattr(
        update_member_presenter.user_repo,
        "users",
        [admin, *update_member_presenter.user_repo.users[1:]],
    )
    member = update_member_presenter.repo.members[0]
    event = {
        "headers": {},
        "queryStringParameters": None,
        "requestContext": {
            "authorizer": {
                "user": json.dumps(
                    {
                        "sub": str(admin.id),
                        "mail": admin.email,
                        "name": admin.user_name,
                    }
                )
            }
        },
        "body": json.dumps(
            {
                "member_id": str(member.member_id),
                "new_member_photo": "https://picsum.photos/800/600.jpg",
                "new_member_name": "updated_name",
                "new_member_intro": "updated_intro",
            }
        ),
    }

    response = update_member_presenter.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["member_id"] == str(member.member_id)
    assert body["member_name"] == "updated_name"
    assert body["member_intro"] == "updated_intro"
    assert body["message"] == "the member was updated successfully"
