import boto3
import dotenv
from src.shared.infra.repositories.project_repository_dynamo import ProjectRepositoryDynamo
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.environments import Environments


def setup_dynamo_table():
    dynamo_table_name = "user_mss_template-table"
    endpoint_url = "http://localhost:8000"
    print("Setting up DynamoDB table...")

    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url)
    print("DynamoDB client created")
    tables = dynamo_client.list_tables()['TableNames']

    if dynamo_table_name not in tables:
        print("Creating table...")
        dynamo_client.create_table(
            TableName=dynamo_table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'
                }

            ],
            BillingMode='PAY_PER_REQUEST',
        )
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=dynamo_table_name)

        print(f'Table "{dynamo_table_name}" created!')

    else:
        print("Table already exists!")


def load_mock_to_local_dynamo():
    setup_dynamo_table()
    mock_repo = ProjectRepositoryMock()
    dynamo_repo = ProjectRepositoryDynamo()

    count = 0

    print('Loading mock data to dynamo...')
    for project in mock_repo.projects:
        print(f"Loading project {project.id} | {project.title} to dynamo")
        dynamo_repo.create_project(project)
        count += 1

    print(f"{count} projects loaded to dynamo!")

def load_mock_to_real_dynamo():
    mock_repo = ProjectRepositoryMock()
    dynamo_repo = ProjectRepositoryDynamo()

    count = 0

    print('Loading mock data to dynamo...')
    for project in mock_repo.projects:
        print(f"Loading project {project.id} | {project.title} to dynamo")
        dynamo_repo.create_project(project)
        count += 1

    print(f"{count} projects loaded to dynamo!")

if __name__ == '__main__':
    dotenv.load_dotenv()
    load_mock_to_local_dynamo()