from typing import List

from pydantic import BaseModel, ConfigDict

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum

class UserViewmodel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    email: str
    role :RoleEnum

    def __init__(self, user: User):
        super().__init__(email=user.email, role=user.role)

    def to_dict(self):
        return self.model_dump()

class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_viewmodel_list = [UserViewmodel(user) for user in users_list]

    def to_dict(self):
        return {
            "all_users": [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
            "message": "all users has been retrieved"
        }
