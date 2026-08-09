from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum

class UserViewmodel:
    def __init__(self, user: User):
        self.role = user.role
        self.email = user.email

    def to_dict(self):
        return {
            'email': self.email,
            'role': self.role.value
        }


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_viewmodel_list = [UserViewmodel(user) for user in users_list]

    def to_dict(self):
        return {
            "all_users": [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
            "message": "all users has been retrieved"
        }
