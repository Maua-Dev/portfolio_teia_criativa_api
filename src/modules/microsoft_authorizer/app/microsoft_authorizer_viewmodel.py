from src.shared.domain.entities.user import User


class MicrosoftAuthorizerViewmodel():
    def __init__(self, was_created: bool):
        self.was_created = was_created

    def to_dict(self):

        if not self.was_created:
            return {
            'message': "the user was retrieved successfully"
            }

        return {
            'message': "the user was created successfully"
            }
