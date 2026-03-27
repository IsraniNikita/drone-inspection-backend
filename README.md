# Drone Inspection Backend

A **serverless backend** for managing drone inspections, built with **AWS Lambda, API Gateway, DynamoDB, and S3**. This project demonstrates a full-stack serverless approach, leveraging best practices in **single-table DynamoDB design, pre-signed S3 uploads, and IAM-based security**.

---

## 🔗 Live API Endpoints

You can directly test these endpoints in Postman or any REST client:

- **Create Inspection**  
  `POST https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev/inspections`

- **List Warehouse Inspections**  
  `GET https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev/inspections/warehouse?warehouse_id=W1`

- **List Drone Inspections**  
  `GET https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev/inspections/drone?drone_id=D1`

- **Generate Upload URL**  
  `POST https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev/inspections/upload-url`

- **List Inspection Images**  
  `GET https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev/inspections/images?inspection_id=e47a4c66-4ad9-4660-bebb-330f84486fb6`

---

## 🚀 Features

- Create inspections for warehouses and drones  
- List inspections by warehouse or drone  
- Upload inspection images directly to S3 via **pre-signed URLs**  
- List images for a specific inspection  
- Proper **error handling** and HTTP status codes  
- Fully serverless, no credentials stored in code  

---

## 🏗 Architecture

```text
Client
   │
   ▼
API Gateway → Lambda Functions → DynamoDB / S3
```

---

## Components:

- API Gateway: Exposes RESTful endpoints
- AWS Lambda: Business logic for all endpoints
- DynamoDB: Single-table design for inspections, warehouses, drones, and images
- S3: Stores inspection images (upload via pre-signed URLs)
- IAM: Provides secure access, no hardcoded credentials

---

## 📊 DynamoDB Data Model

**Table Name:** drone-inspections
**Partition Key:** PK (String)
**Sort Key:** SK (String)
**Global Secondary Index (GSI1):**

- GSI1PK (String)
- GSI1SK (String)

### Entities & Access Patterns
1. Warehouse → Inspections (1:N)
- PK: WAREHOUSE#{warehouse_id}
- SK: INSPECTION#{inspection_id}
- GSI1PK: DRONE#{drone_id}
- GSI1SK: INSPECTION#{timestamp}
2. Inspection → Images (1:N)
- PK: INSPECTION#{inspection_id}
- SK: IMAGE#{image_id}
3. Drone Mapping
PK: WAREHOUSE#{warehouse_id}
SK: DRONE#{drone_id}

---

## 🛠 Deployment Steps (Detailed)
1️⃣ DynamoDB Table
- Create Table → drone-inspections
  - Partition Key: PK (String)
  - Sort Key: SK (String)
- Create GSI (GSI1)
  - Partition Key: GSI1PK
  - Sort Key: GSI1SK
  - Projection: All

2️⃣ S3 Bucket
- Create bucket (e.g., drone-inspection-images-nikita-123)
- Region: ap-south-1
- Disable Block all public access, acknowledge warning

3️⃣ Lambda Functions
- create function → Author from scratch → Python 3.9
- write respective handler code (create_inspection.py, etc.)
- Add environment variables:
  - TABLE_NAME = drone-inspections
  - BUCKET_NAME = your-bucket-name
- Attach policies:
  - AmazonDynamoDBFullAccess
  - AmazonS3FullAccess

Repeat for all 5 handlers

4️⃣ API Gateway (HTTP API)
- Add integration → Lambda → choose function
- Define routes as listed above
- Deploy API → get base URL: https://2b0metsboa.execute-api.ap-south-1.amazonaws.com/dev

---

## ✅ IAM & Security
- No credentials in code
- Lambdas have minimal required IAM roles:
- DynamoDB: PutItem, Query
- S3: PutObject
- Pre-signed URLs secure direct client uploads

---

## 💡 Key Learnings
- Efficient single-table design in DynamoDB
- Secure file uploads with S3 pre-signed URLs
- Proper error handling & status codes
- Serverless best practices with Lambda + API Gateway + IAM

