from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

# Manter alinhado com src.shared.infra.external.dynamo/..._naming/..._TABLE_PREFIX
_PORTFOLIOTEIA_TABLE_PREFIX = "PortfolioTeiaCriativaTable"

RETAINED_STAGES = {"prod", "homolog"}


class DynamoConstruct(Construct):

    portfolioTeiaCriativa_table: dynamodb.Table

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        removal_policy = (
            RemovalPolicy.RETAIN if stage_lower in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        self.portfolioTeiaCriativa_table = dynamodb.Table(
            self,
            id="PortfolioTeiaCriativaTable",
            partition_key=dynamodb.Attribute(
                name="pk", # NOTE: PK_ATTR dentro de external/dynamo_keys deve estar condizente com essa linha
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="sk", # NOTE: SK_ATTR dentro de external/dynamo_keys deve estar condizente com essa linha
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            table_name=f"{_PORTFOLIOTEIA_TABLE_PREFIX}-{stage_lower}",
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=(stage_lower == "prod")
            ),
        )

        # GSI denso: buscar user por email (alinhado a dynamo_keys.GSI2_NAME)
        self.portfolioTeiaCriativa_table.add_global_secondary_index(
            index_name="UserEmailIndex",
            partition_key=dynamodb.Attribute(
                name="gsi2pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="gsi2sk",
                type=dynamodb.AttributeType.STRING,
            ),
            projection_type=dynamodb.ProjectionType.ALL,
        )