import uuid

from src.modules.member.delete_member.app.delete_member_controller import DeleteMemberController
from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


def create_controller():
    repo = MemberRepositoryMock()
    return DeleteMemberController(DeleteMemberUsecase(repo)), repo


class TestDeleteMemberController:
    def test_delete_member_controller(self):
        controller, repo = create_controller()
        member = repo.members[0]

        response = controller(
            HttpRequest(body={"member_id": str(member.member_id)})
        )

        assert response.status_code == 200
        assert response.body["member_id"] == str(member.member_id)
        assert response.body["message"] == "the member was deleted successfully"
        assert member not in repo.members

    def test_delete_member_controller_missing_parameter(self):
        controller, _ = create_controller()

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == "Field member_id is missing"

    def test_delete_member_controller_wrong_type(self):
        controller, _ = create_controller()

        response = controller(HttpRequest(body={"member_id": 123}))

        assert response.status_code == 400
        assert response.body == (
            "The field 'member_id' has the wrong type. "
            "Received: 'int'. Expected: 'str'."
        )

    def test_delete_member_controller_invalid_id(self):
        controller, _ = create_controller()

        response = controller(HttpRequest(body={"member_id": "invalid"}))

        assert response.status_code == 400
        assert response.body == "Field member_id is not valid"

    def test_delete_member_controller_not_found(self):
        controller, _ = create_controller()

        response = controller(HttpRequest(body={"member_id": str(uuid.uuid4())}))

        assert response.status_code == 404
        assert response.body == "No items found for member_id"
