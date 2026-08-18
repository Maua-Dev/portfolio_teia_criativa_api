import uuid

from src.modules.get_all_projects.app.get_all_projects_viewmodel import GetAllProjectsViewmodel, ProjectViewmodel
from src.shared.domain.entities.project import Project


class Test_GetAllProjectsViewmodel:
    project_id_1 = uuid.UUID("2b6e8583-205f-4865-ae83-6ddb8fc58f03")
    project_id_2 = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")

    all_projects_list = [
        Project(
            id=project_id_1,
            title="dev medias",
            description="Projeto de organização de notas dos alunos",
        ),
        Project(
            id=project_id_2,
            title="teia criativa",
            description="Plataforma colaborativa de projetos",
        ),
    ]

    def test_get_all_projects_viewmodel(self):
        viewmodel = GetAllProjectsViewmodel(self.all_projects_list)

        expected = {
            "all_projects": [
                {
                    'project_id': str(self.project_id_1),
                    'title': "Dev medias",
                    'description': "Projeto de organização de notas dos alunos",
                    'associates': None,
                    'display_image': None,
                },
                {
                    'project_id': str(self.project_id_2),
                    'title': "Teia criativa",
                    'description': "Plataforma colaborativa de projetos",
                    'associates': None,
                    'display_image': None,
                }
            ],
            "message": "all projects has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_project_viewmodel(self):
        viewmodel = ProjectViewmodel(
            Project(
                id=self.project_id_2,
                title="teia criativa",
                description="Plataforma colaborativa de projetos",
            ),
        )

        response = viewmodel.to_dict()

        expected = {
            'project_id': str(self.project_id_2),
            'title': "Teia criativa",
            'description': "Plataforma colaborativa de projetos",
            'associates': None,
            'display_image': None,
        }

        assert response == expected