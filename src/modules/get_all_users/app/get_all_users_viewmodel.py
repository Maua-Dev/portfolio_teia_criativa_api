from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class UserViewmodel:
    id: str
    email: str
    role: RoleEnum

    def __init__(self, user: User):
        self.id = str(user.id)
        self.email = user.email
        self.role = user.role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value if hasattr(self.role, "value") else str(self.role),
        }


class GetAllUsersViewModel:
    users: List[UserViewmodel]

    def __init__(self, users: List[User]):
        self.users = [UserViewmodel(user) for user in users]

    def to_dict(self) -> dict:
        return {
            "users": [user.to_dict() for user in self.users],
            "message": "the users were retrieved"
        }

GetAllUsersViewmodel = GetAllUsersViewModel