import uuid

from src.modules.member.update_member.app.update_member_controller import UpdateMemberController
from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


def create_controller():
    repo = MemberRepositoryMock()
    return UpdateMemberController(UpdateMemberUsecase(repo)), repo


class TestUpdateMemberController:
    def test_updates_member_and_returns_viewmodel(self):
        controller, repo = create_controller()
        member = repo.members[0]

        response = controller(
            HttpRequest(
                body={
                    "member_id": str(member.member_id),
                    "new_member_name": "Updated name",
                }
            )
        )

        assert response.status_code == 200
        assert response.body == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": "Updated name",
            "member_intro": member.member_intro,
            "message": "the member was updated successfully",
        }

    def test_requires_member_id(self):
        controller, _ = create_controller()

        response = controller(HttpRequest(body={"new_member_name": "Updated name"}))

        assert response.status_code == 400
        assert response.body == "Field member_id is missing"

    def test_requires_at_least_one_update_field(self):
        controller, repo = create_controller()

        response = controller(
            HttpRequest(body={"member_id": str(repo.members[0].member_id)})
        )

        assert response.status_code == 400
        assert response.body == (
            "Field new_member_photo, new_member_name, or new_member_intro is missing"
        )

    def test_rejects_wrong_update_field_type(self):
        controller, repo = create_controller()

        response = controller(
            HttpRequest(
                body={
                    "member_id": str(repo.members[0].member_id),
                    "new_member_name": 123,
                }
            )
        )

        assert response.status_code == 400
        assert response.body == (
            "The field 'new_member_name' has the wrong type. "
            "Received: 'int'. Expected: 'str'."
        )

    def test_returns_not_found_for_unknown_member(self):
        controller, _ = create_controller()

        response = controller(
            HttpRequest(
                body={
                    "member_id": str(uuid.uuid4()),
                    "new_member_intro": "Updated intro",
                }
            )
        )

        assert response.status_code == 404
        assert response.body == "No items found for member_id"
