from src.shared.domain.entities.project import Project
import uuid


class DeleteProjectViewmodel:
    id: uuid.UUID
    title: str
    description: str
    associates: list[uuid.UUID]
    display_image: str

    def __init__(self, project: Project):
        self.id = project.id
        self.title = project.title
        self.description = project.description
        self.associates = project.associates
        self.display_image = project.display_image

    def to_dict(self):
        return {
            'project_id': str(self.id),
            'title': self.title,
            'description': self.description,
            'associates': self.associates,
            'display_image': self.display_image,
            'message': "the project was deleted successfully"
        }