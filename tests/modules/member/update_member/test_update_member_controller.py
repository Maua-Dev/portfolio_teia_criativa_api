from src.modules.member.update_member.app.update_member_controller import UpdateMemberController
from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def _create_controller():
    member_repo = MemberRepositoryMock()
    user_repo = UserRepositoryMock()
    admin = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    user_repo.users[0] = admin
    return (
        UpdateMemberController(UpdateMemberUsecase(member_repo, user_repo)),
        member_repo,
        admin,
    )


def _request(member_id, requester_id, **body):
    request = HttpRequest(body={"member_id": member_id, **body})
    if requester_id is not None:
        request.data[USER_FROM_AUTHORIZER_KEY] = {"sub": requester_id}
    return request


def test_update_member_controller():
    controller, member_repo, admin = _create_controller()
    member_id = str(member_repo.members[0].member_id)

    response = controller(
        _request(
            member_id,
            str(admin.id),
            new_member_photo="https://picsum.photos/800/600.jpg",
            new_member_name="updated_name",
            new_member_intro="updated_intro",
        )
    )

    assert response.status_code == 200
    assert response.body["member_id"] == member_id
    assert response.body["member_name"] == "updated_name"
    assert response.body["member_intro"] == "updated_intro"
    assert response.body["message"] == "the member was updated successfully"


def test_update_member_controller_rejects_invalid_photo_url():
    controller, member_repo, admin = _create_controller()

    response = controller(
        _request(
            str(member_repo.members[0].member_id),
            str(admin.id),
            new_member_photo="https://example.com/image.bmp",
            new_member_name="updated_name",
            new_member_intro="updated_intro",
        )
    )

    assert response.status_code == 400
    assert response.body.startswith("new_member_photo must be a valid URL")


def test_update_member_controller_requires_authenticated_requester():
    controller, member_repo, _ = _create_controller()

    response = controller(
        _request(
            str(member_repo.members[0].member_id),
            None,
            new_member_photo="https://picsum.photos/800/600.jpg",
            new_member_name="updated_name",
            new_member_intro="updated_intro",
        )
    )

    assert response.status_code == 400
    assert response.body == "Field requester_id is not valid"
