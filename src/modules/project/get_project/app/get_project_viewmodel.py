from src.shared.domain.entities.project import Project
import uuid


class GetProjectViewmodel:
    id: uuid.UUID
    title: str
    description: str

    def __init__(self, project: Project):
        self.id = project.id
        self.title = project.title
        self.description = project.description

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'message': "the project was retrieved successfully"
        }
