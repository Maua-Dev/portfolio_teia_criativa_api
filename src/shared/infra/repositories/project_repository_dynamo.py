from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.project_dynamo_dto import ProjectDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class ProjectRepositoryDynamo(IProjectRepository):

    @staticmethod
    def partition_key_format(project_id) -> str:
        return f"project#{project_id}"

    @staticmethod
    def sort_key_format(project_id) -> str:
        return f"#{project_id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key)

    def get_project(self, project_id: str) -> Project:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(project_id), sort_key=self.sort_key_format(project_id))

        if resp.get('Item') is None:
            raise NoItemsFound("project_id")

        project_dto = ProjectDynamoDTO.from_dynamo(resp["Item"])
        return project_dto.to_entity()

    def get_all_project(self) -> list[Project]:
        resp = self.dynamo.get_all_items()
        projects = []
        for item in resp['Items']:
            if item.get("entity") == 'project':
                projects.append(ProjectDynamoDTO.from_dynamo(item).to_entity())

        return projects

    def create_project(self, new_project: Project) -> Project:
        project_dto = ProjectDynamoDTO.from_entity(project=new_project)
        resp = self.dynamo.put_item(partition_key=self.partition_key_format(new_project.id),
                                    sort_key=self.sort_key_format(new_project.id),
                                    item=project_dto.to_dynamo())
        return new_project

    def delete_project(self, project_id: str) -> Project:
        resp = self.dynamo.delete_item(partition_key=self.partition_key_format(project_id), sort_key=self.sort_key_format(project_id))

        if "Attributes" not in resp:
            raise NoItemsFound("project_id")

        return ProjectDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def update_project(self, project_id: str, new_title: str = None, new_description: str = None, new_display_image: str = None) -> Project:
        project = self.get_project(project_id=project_id)

        item_to_update = {}

        if new_title:
            item_to_update['title'] = new_title
        if new_description:
            item_to_update['description'] = new_description
        if new_display_image:
            item_to_update['display_image'] = new_display_image

        if not item_to_update:
            raise NoItemsFound("Nothing to update")

        resp = self.dynamo.update_item(partition_key=self.partition_key_format(project_id),
                                        sort_key=self.sort_key_format(project_id),
                                        update_dict=item_to_update)

        return ProjectDynamoDTO.from_dynamo(resp['Attributes']).to_entity()