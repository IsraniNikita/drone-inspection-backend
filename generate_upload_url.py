import json
import os
import uuid
import time
import boto3
from decimal import Decimal

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
            
        inspection_id = data.get("inspection_id")
        
        if not inspection_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing inspection_id"})
            }
            
      
        image_id = str(uuid.uuid4())
        timestamp = int(time.time())
        
        
        s3_key = f"inspection-images/{inspection_id}/{image_id}.jpg"
        
       
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key,
                "ContentType": "image/jpeg" 
            },
            ExpiresIn=3600
        )
        
       
        item = {
            "PK": f"INSPECTION#{inspection_id}",
            "SK": f"IMAGE#{image_id}",
            "image_id": image_id,
            "inspection_id": inspection_id,
            "s3_key": s3_key,
            "created_at": timestamp,
            "status": "PENDING"
        }
        
        table.put_item(Item=item)
        
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Upload URL generated successfully",
                "upload_url": url,
                "image": item
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }