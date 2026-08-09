import uuid

from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(user_id=1,
             senha_hash=str(uuid.uuid4()),
             name="Lucas Duez",
             email="deuzexmachina@gmail.com",
             role=RoleEnum.ADMIN),

        User(user_id=2,
             senha_hash=str(uuid.uuid4()),
             name="Laura Blablachan",
             email="laurinha@gmail.com",
             role=RoleEnum.USER),
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'email': "deuzexmachina@gmail.com",
                    'role': RoleEnum.ADMIN.value,
                },
                {
                    'email': "laurinha@gmail.com",
                    'role': RoleEnum.USER.value,
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(user_id=2,
                 senha_hash=str(uuid.uuid4()),
                 name="Laura Blablachan",
                 email="laurinha@gmail.com",
                 role=RoleEnum.USER),
)

        response = viewmodel.to_dict()

        expected = {
                    'email': "laurinha@gmail.com",
                    'role': RoleEnum.USER.value,
        }

        assert response == expected


    
