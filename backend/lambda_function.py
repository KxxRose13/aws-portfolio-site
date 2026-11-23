import json
import logging
import os
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("TABLE_NAME", "PortfolioVisitorCounter")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


class DecimalEncoder(json.JSONEncoder):
    """Convert DynamoDB Decimal values into JSON-compatible numbers."""

    def default(self, value):
        if isinstance(value, Decimal):
            if value % 1 == 0:
                return int(value)

            return float(value)

        return super().default(value)


def build_response(status_code, body):
    """Create a response that can later be returned through API Gateway."""

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body, cls=DecimalEncoder)
    }


def lambda_handler(event, context):
    """Increment and return the portfolio visitor count."""

    logger.info(
        "Visitor counter invoked. Request ID: %s",
        context.aws_request_id if context else "local-test"
    )

    try:
        response = table.update_item(
            Key={
                "id": "portfolio"
            },
            UpdateExpression=(
                "SET #visitor_count = "
                "if_not_exists(#visitor_count, :zero) + :increment"
            ),
            ExpressionAttributeNames={
                "#visitor_count": "count"
            },
            ExpressionAttributeValues={
                ":zero": 0,
                ":increment": 1
            },
            ReturnValues="UPDATED_NEW"
        )

        updated_count = response["Attributes"]["count"]

        logger.info("Visitor count updated to %s", updated_count)

        return build_response(
            200,
            {
                "message": "Visitor count updated successfully.",
                "count": updated_count
            }
        )

    except ClientError as error:
        logger.exception("DynamoDB rejected the visitor counter update.")

        return build_response(
            500,
            {
                "message": "Unable to update visitor count.",
                "error": error.response["Error"]["Code"]
            }
        )

    except Exception:
        logger.exception("Unexpected visitor counter error.")

        return build_response(
            500,
            {
                "message": "An unexpected error occurred."
            }
        )