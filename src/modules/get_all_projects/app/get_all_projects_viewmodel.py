from typing import List
from src.shared.domain.entities.project import Project


class ProjectViewmodel:
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
            'display_image': self.display_image
        }


class GetAllProjectsViewmodel:
    def __init__(self, projects_list: List[Project]):
        self.projects_viewmodel_list = [ProjectViewmodel(project) for project in projects_list]

    def to_dict(self):
        return {
            "all_projects": [viewmodel.to_dict() for viewmodel in self.projects_viewmodel_list],
            "message": "all projects has been retrieved"
        }
