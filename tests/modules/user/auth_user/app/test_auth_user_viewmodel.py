import uuid

from src.modules.user.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_AuthUserViewmodel:

    def test_auth_user_viewmodel_created(self):
        user = User(
            id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
            email="teste@maua.br",
            role=RoleEnum.USER,
            user_name="user_name_test1",
        )
        viewmodel = AuthUserViewmodel(user=user, case_number=1)

        assert viewmodel.to_dict() == {
            "id": "af852f40-0135-406d-b5d7-7ed5dce9bc8e",
            "email": "teste@maua.br",
            "role": RoleEnum.USER.value,
            "active": True,
            "user_name": "user_name_test1",
            "message": "the user was created successfully",
        }

    def test_auth_user_viewmodel_retrieved(self):
        user = User(
            id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
            email="teste@maua.br",
            role=RoleEnum.USER,
            user_name="user_name_test1",
        )
        viewmodel = AuthUserViewmodel(user=user, case_number=0)

        assert viewmodel.to_dict() == {
            "id": "af852f40-0135-406d-b5d7-7ed5dce9bc8e",
            "email": "teste@maua.br",
            "role": RoleEnum.USER.value,
            "active": True,
            "user_name": "user_name_test1",
            "message": "the user was retrieved successfully",
        }
