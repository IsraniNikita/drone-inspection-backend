import json
import os
import uuid
import time
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

TABLE_NAME = os.environ.get("TABLE_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        inspection_id = params.get("inspection_id")
        
        if not inspection_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing inspection_id query parameter"})
            }
            
        response = table.query(
            
            KeyConditionExpression=Key("PK").eq(f"INSPECTION#{inspection_id}") & Key("SK").begins_with("IMAGE#")
        )
        
        items = response.get("Items", [])
        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No images found for this inspection"})
            }
            
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "images": items
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }