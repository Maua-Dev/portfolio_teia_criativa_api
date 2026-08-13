from src.modules.create_project.app.create_project_viewmodel import CreateProjectViewmodel
from src.shared.domain.entities.project import Project
import uuid

class Test_CreateProjectViewModel:
    def test_create_project_viewmodel(self):
        id = uuid.UUID("2b6e8583-205f-4865-ae83-6ddb8fc58f03")

        project = Project(
            id=id,
            title="Dev Médias",
            description="Projeto de organização de notas dos alunos",
        )
        projectViewmodel = CreateProjectViewmodel(project=project).to_dict()

        expected = {
            'id': id,
            'title': 'Dev médias',
            'description': 'Projeto de organização de notas dos alunos',
            'associates': None,
            'display_image': None,
            'message': 'the project was created successfully'
        }

        assert expected == projectViewmodel