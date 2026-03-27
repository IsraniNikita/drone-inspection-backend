import json
import os
import uuid
import time
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ.get("TABLE_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Empty request body"})
            }
            
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON format"})
            }
            
        warehouse_id = data.get("warehouse_id")
        drone_id = data.get("drone_id")
        
        if not warehouse_id or not drone_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing warehouse_id or drone_id"})
            }
            
        inspection_id = str(uuid.uuid4())
        timestamp = int(time.time())
        
        item = {
            "PK": f"WAREHOUSE#{warehouse_id}",
            "SK": f"INSPECTION#{inspection_id}",
            "GSI1PK": f"DRONE#{drone_id}",
            "GSI1SK": f"INSPECTION#{timestamp}",
            "inspection_id": inspection_id,
            "warehouse_id": warehouse_id,
            "drone_id": drone_id,
            "created_at": timestamp,
            "status": "CREATED"
        }
        
        table.put_item(Item=item)
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Inspection created successfully",
                "inspection": item
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
