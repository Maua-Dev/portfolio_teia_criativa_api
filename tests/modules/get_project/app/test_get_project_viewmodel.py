from src.modules.get_project.app.get_project_viewmodel import GetProjectViewmodel
from src.shared.domain.entities.project import Project
import uuid

class Test_GetProjectViewModel:
    def test_get_project_viewmodel(self):
        id = uuid.UUID("2b6e8583-205f-4865-ae83-6ddb8fc58f03")
        project = Project(
            id=id,
            title="Dev Médias",
            description="Projeto de organização de notas dos alunos"
        )
        userViewmodel = GetProjectViewmodel(project=project).to_dict()

        expected = {'id': str(id),
                    'title':"Dev médias",
                    'description':"Projeto de organização de notas dos alunos",
                    'message': 'the project was retrieved successfully'}

        assert expected == userViewmodel
