from src.modules.project.create_project.app.create_project_viewmodel import CreateProjectViewmodel
from src.shared.domain.entities.project import Project


class Test_CreateProjectViewModel:
    def test_create_project_viewmodel(self):
        project = Project(
            title="Novo projeto",
            description="Projeto criado no teste",
        )
        viewmodel = CreateProjectViewmodel(project).to_dict()

        expected = {
            'id': str(project.id),
            'title': project.title,
            'description': project.description,
            'associates': None,
            'display_image': None,
            'message': 'the project was created successfully',
        }

        assert expected == viewmodel
