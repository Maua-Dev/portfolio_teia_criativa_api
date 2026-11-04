import uuid

from src.modules.get_member.app.get_member_controller import GetMemberController
from src.modules.get_member.app.get_member_usecase import GetMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


def create_controller(repo=None):
    repo = repo or MemberRepositoryMock()
    observability = ObservabilityMock(module_name="get_member")
    return GetMemberController(
        GetMemberUsecase(repo=repo, observability=observability),
        observability=observability,
    ), repo


class Test_GetMemberController:
    def test_get_member_controller(self):
        controller, repo = create_controller()
        member = repo.members[0]

        response = controller(
            request=HttpRequest(query_params={"member_id": str(member.member_id)})
        )

        assert response.status_code == 200
        assert response.body["member_id"] == str(member.member_id)
        assert response.body["member_name"] == member.member_name
        assert response.body["message"] == "the member was retrieved successfully"

    def test_get_member_controller_missing_parameter(self):
        controller, _ = create_controller()

        response = controller(request=HttpRequest(query_params={}))

        assert response.status_code == 400
        assert response.body == "Field member_id is missing"

    def test_get_member_controller_wrong_type_parameter(self):
        controller, _ = create_controller()

        response = controller(request=HttpRequest(query_params={"member_id": 123}))

        assert response.status_code == 400
        assert response.body == (
            "The field 'member_id' has the wrong type. "
            "Received: 'int'. Expected: 'str'."
        )

    def test_get_member_controller_invalid_id(self):
        controller, _ = create_controller()

        response = controller(
            request=HttpRequest(query_params={"member_id": "invalid"})
        )

        assert response.status_code == 400
        assert response.body == "Field member_id is not valid"

    def test_get_member_controller_not_found(self):
        controller, _ = create_controller()

        response = controller(
            request=HttpRequest(query_params={"member_id": str(uuid.uuid4())})
        )

        assert response.status_code == 404
        assert response.body == "No items found for member_id"
