import uuid

from src.modules.member.delete_member.app.delete_member_controller import DeleteMemberController
from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def create_controller(role=RoleEnum.ADMIN, active=True):
    member_repo = MemberRepositoryMock()
    user_repo = UserRepositoryMock()
    user_repo.users[0] = user_repo.users[0].model_copy(
        update={"role": role, "active": active}
    )
    usecase = DeleteMemberUsecase(repo=member_repo, user_repo=user_repo)
    return DeleteMemberController(usecase=usecase), member_repo, user_repo


def create_request(body, requester_id="af852f40-0135-406d-b5d7-7ed5dce9bc8e"):
    request = HttpRequest(body=body)
    request.data[USER_FROM_AUTHORIZER_KEY] = {"sub": requester_id}
    return request


class TestDeleteMemberController:
    def test_delete_member_controller(self):
        controller, member_repo, _ = create_controller()
        member = member_repo.members[0]

        response = controller(
            create_request({"member_id": str(member.member_id)})
        )

        assert response.status_code == 200
        assert response.body == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": member.member_name,
            "member_intro": member.member_intro,
            "message": "the member was deleted successfully",
        }
        assert member not in member_repo.members

    def test_delete_member_controller_missing_member_id(self):
        controller, _, _ = create_controller()

        response = controller(create_request({}))

        assert response.status_code == 400
        assert response.body == "Field member_id is missing"

    def test_delete_member_controller_wrong_member_id_type(self):
        controller, _, _ = create_controller()

        response = controller(create_request({"member_id": 123}))

        assert response.status_code == 400
        assert response.body == (
            "The field 'member_id' has the wrong type. "
            "Received: 'int'. Expected: 'str'."
        )

    def test_delete_member_controller_invalid_member_id(self):
        controller, _, _ = create_controller()

        response = controller(create_request({"member_id": "not-a-uuid"}))

        assert response.status_code == 400
        assert response.body == "Field member_id is not valid"

    def test_delete_member_controller_member_not_found(self):
        controller, _, _ = create_controller()

        response = controller(create_request({"member_id": str(uuid.uuid4())}))

        assert response.status_code == 404
        assert response.body == "No items found for member_id"

    def test_delete_member_controller_forbidden_for_non_admin(self):
        controller, member_repo, _ = create_controller(role=RoleEnum.USER)
        member = member_repo.members[0]

        response = controller(
            create_request({"member_id": str(member.member_id)})
        )

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this Delete Member"
        assert member in member_repo.members

    def test_delete_member_controller_forbidden_for_inactive_admin(self):
        controller, member_repo, _ = create_controller(active=False)
        member = member_repo.members[0]

        response = controller(
            create_request({"member_id": str(member.member_id)})
        )

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this Delete Member"
        assert member in member_repo.members

    def test_delete_member_controller_without_authenticated_user(self):
        controller, member_repo, _ = create_controller()
        member = member_repo.members[0]
        request = HttpRequest(body={"member_id": str(member.member_id)})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field requester_id is not valid"
        assert member in member_repo.members
