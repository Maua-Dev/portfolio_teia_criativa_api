import uuid

from src.modules.delete_project.app.delete_project_viewmodel import DeleteProjectViewmodel
from src.shared.domain.entities.project import Project


class Test_DeleteProjectViewmodel:
    def test_delete_project_viewmodel(self):
        id = uuid.UUID("2b6e8583-205f-4865-ae83-6ddb8fc58f03")

        project = Project(
            id=id,
            title="dev medias",
            description="Projeto de organização de notas dos alunos",
            associates=None,
            display_image=None
        )

        delete_project_viewmodel = DeleteProjectViewmodel(project)

        expected = {
            'project_id': str(id),
            'title': 'Dev medias',
            'description': 'Projeto de organização de notas dos alunos',
            'associates': None,
            'display_image': None,
            'message': 'the project was deleted successfully'
        }

        assert expected == delete_project_viewmodel.to_dict()