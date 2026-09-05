import uuid

from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
             email="deuzexmachina@gmail.com",
             role=RoleEnum.ADMIN,
             active=True,
             user_name="username_test1"),

        User(id=uuid.UUID("b9a52f40-0135-406d-b5d7-7ed5dce9bc8f"),
             email="laurinha@gmail.com",
             role=RoleEnum.USER,
             active=False,
             user_name="username_test2")
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'email': "deuzexmachina@gmail.com",
                    'role': RoleEnum.ADMIN.value,
                    'active': True,
                    'user_name': "username_test1"
                },
                {
                    'email': "laurinha@gmail.com",
                    'role': RoleEnum.USER.value,
                    'active': False,
                    'user_name': "username_test2"
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(id=uuid.UUID("b9a52f40-0135-406d-b5d7-7ed5dce9bc8f"),
                 senha_hash="hash_fake_2",
                 email="laurinha@gmail.com",
                 role=RoleEnum.USER,
                 active=True,
                 user_name="username_test3"),
)

        response = viewmodel.to_dict()

        expected = {
                    'email': "laurinha@gmail.com",
                    'role': RoleEnum.USER.value,
                    'active': True,
                    'user_name': "username_test3"
        }

        assert response == expected


    
