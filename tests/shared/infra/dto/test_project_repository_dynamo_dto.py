import uuid

from src.shared.domain.entities.project import Project
from src.shared.infra.dto.project_dynamo_dto import ProjectDynamoDTO
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class Test_ProjectRepositoryDTO:
    def test_from_entity(self):
        repo = ProjectRepositoryMock()

        project_dto = ProjectDynamoDTO.from_entity(project=repo.projects[0])

        expected_selfie_dto = ProjectDynamoDTO(
            title=repo.projects[0].title,
            description=repo.projects[0].description,
            associates=repo.projects[0].associates,
            display_image=repo.projects[0].display_image,
            id=repo.projects[0].id
        )

        assert project_dto == expected_selfie_dto

    def test_to_dynamo(self):
        repo = ProjectRepositoryMock()

        project_dto = ProjectDynamoDTO(
            title=repo.projects[0].title,
            description=repo.projects[0].description,
            associates=repo.projects[0].associates,
            display_image=repo.projects[0].display_image,
            id=repo.projects[0].id
        )

        project_dynamo = project_dto.to_dynamo()

        expected_dict = {
            "entity": "project",
            "title": repo.projects[0].title,
            "description": repo.projects[0].description,
            "associates": [str(a) for a in repo.projects[0].associates] if repo.projects[0].associates else [],
            "display_image": repo.projects[0].display_image,
            "id": str(repo.projects[0].id)
        }

        assert project_dto.to_dynamo() == expected_dict

    def test_from_dynamo(self):
        repo = ProjectRepositoryMock()

        project_id = uuid.uuid4()
        associate_id = uuid.uuid4()

        dynamo_dict = {'Item': {'id': str(project_id),
                            'title': 'Meu Projeto',
                            'SK': f'#{project_id}',
                            'PK': f'project#{project_id}',
                            'entity': 'project',
                            'description': 'Descrição do projeto',
                            'associates': [str(associate_id)],
                            'display_image': 'https://exemplo.com/imagem.png'},
                    'ResponseMetadata': {'RequestId': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                        'HTTPStatusCode': 200,
                                        'HTTPHeaders': {'date': 'Fri, 16 Dec 2022 15:40:29 GMT',
                                                        'content-type': 'application/x-amz-json-1.0',
                                                        'x-amz-crc32': '3909675734',
                                                        'x-amzn-requestid': 'aa6a5e5e-943f-4452-8c1f-4e5441ee6042',
                                                        'content-length': '174',
                                                        'server': 'Jetty(9.4.48.v20220622)'},
                                        'RetryAttempts': 0}}

        project_dto = ProjectDynamoDTO.from_dynamo(project_data=dynamo_dict["Item"])

        expected_project_dto = ProjectDynamoDTO(
            title="Meu Projeto",
            description="Descrição do projeto",
            associates=[associate_id],
            display_image="https://exemplo.com/imagem.png",
            id=project_id
        )

        assert project_dto == expected_project_dto

    def test_to_entity(self):
        repo = ProjectRepositoryMock()

        project_dto = ProjectDynamoDTO(
            title=repo.projects[0].title,
            description=repo.projects[0].description,
            associates=repo.projects[0].associates,
            display_image=repo.projects[0].display_image,
            id=repo.projects[0].id
        )

        project = project_dto.to_entity()

        assert project.title == repo.projects[0].title
        assert project.description == repo.projects[0].description
        assert project.associates == repo.projects[0].associates
        assert project.display_image == repo.projects[0].display_image
        assert project.id == repo.projects[0].id

        project_id = uuid.uuid4()
        associate_id = uuid.uuid4()

        dynamo_item = {'Item': {'id': str(project_id),
                                'title': 'Meu Projeto',
                                'SK': f'#{project_id}',
                                'PK': f'project#{project_id}',
                                'entity': 'project',
                                'description': 'Descrição do projeto',
                                'associates': [str(associate_id)],
                                'display_image': 'https://exemplo.com/imagem.png'}}

        project_dto = ProjectDynamoDTO.from_dynamo(project_data=dynamo_item["Item"])

        project = project_dto.to_entity()

        expected_project = Project(
            title="Meu Projeto",
            description="Descrição do projeto",
            associates=[associate_id],
            display_image="https://exemplo.com/imagem.png",
            id=project_id
        )

        assert project.title == expected_project.title
        assert project.description == expected_project.description
        assert project.associates == expected_project.associates
        assert project.display_image == expected_project.display_image
        assert project.id == expected_project.id

    def test_from_entity_to_dynamo(self):
        repo = ProjectRepositoryMock()

        project_dto = ProjectDynamoDTO.from_entity(project=repo.projects[0])

        project_dynamo = project_dto.to_dynamo()

        expected_dict = {
            "entity": "project",
            "title": repo.projects[0].title,
            "description": repo.projects[0].description,
            "associates": [str(a) for a in repo.projects[0].associates] if repo.projects[0].associates else [],
            "display_image": repo.projects[0].display_image,
            "id": str(repo.projects[0].id)
        }

        assert project_dynamo == expected_dict