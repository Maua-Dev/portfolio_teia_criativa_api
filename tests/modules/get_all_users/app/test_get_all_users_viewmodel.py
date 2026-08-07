import uuid
from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_GetAllUsersViewModel:
    def test_get_all_users_viewmodel(self):
        users = [
            User(
                id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
                email="soller@soller.com",
                role=RoleEnum.USER,
                senha_hash="hash_fake_1"
            ),
            User(
                id=uuid.UUID("b9a52f40-0135-406d-b5d7-7ed5dce9bc8f"),
                email="brancas@brancas.com",
                role=RoleEnum.USER,
                senha_hash="hash_fake_2"
            )
        ]

        viewmodel = GetAllUsersViewModel(users)
        response = viewmodel.to_dict()

        assert "users" in response
        assert len(response["users"]) == 2