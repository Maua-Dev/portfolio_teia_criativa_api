import uuid

from src.modules.update_project.app.update_project_viewmodel import UpdateProjectViewmodel
from src.shared.domain.entities.project import Project


class Test_UpdateProjectViewmodel:
    def test_update_project_viewmodel(self):
        project_id = uuid.UUID("2b6e8583-205f-4865-ae83-6ddb8fc58f03")

        project = Project(
            id=project_id,
            title="dev bank",
            description="Projeto do processo seletivo para Dev Community"
        )

        updated_project_viewmodel = UpdateProjectViewmodel(project)

        expected = {
            'project_id': str(project_id),
            'title': "Dev bank",
            'description': "Projeto do processo seletivo para Dev Community",
            'message': "the project was updated successfully"
        }

        assert expected == updated_project_viewmodel.to_dict()