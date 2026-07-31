from src.shared.domain.entities.project import Project
import uuid

class CreateProjectViewmodel:
    id: uuid.UUID
    title: str
    description: str

    def __init__(self, project: Project):
        self.user_id = project.id
        self.title = project.title
        self.description = project.description

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'message': "the project was created successfully"
        }