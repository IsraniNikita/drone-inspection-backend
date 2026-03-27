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
        drone_id = params.get("drone_id")
        
        if not drone_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing drone_id query parameter"})
            }
            
        response = table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1PK").eq(f"DRONE#{drone_id}") & Key("GSI1SK").begins_with("INSPECTION#")
        )
        
        items = response.get("Items", [])
        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No inspections found for this drone"})
            }
            
       
        return {
            "statusCode": 200,
            "body": json.dumps({
                "inspections": items
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }