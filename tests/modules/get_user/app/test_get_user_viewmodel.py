import uuid

from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_GetUserViewModel:
    def test_get_user_viewmodel(self):
        user = User(
            user_id= str(uuid.uuid4()),
            name="Vitor Soller",
            email="vitinho@hype.com",
            role=RoleEnum.USER,
            active=True,
            user_name="username_1"
        )
        userViewmodel = GetUserViewmodel(user=user).to_dict()

        expected = {
                    'email': 'vitinho@hype.com',
                    'role': RoleEnum.USER.value,
                    'active': True,
                    'user_name': "username_1",
                    'message': 'the user was retrieved successfully'}

        assert expected == userViewmodel
