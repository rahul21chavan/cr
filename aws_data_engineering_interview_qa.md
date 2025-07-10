# AWS Data Engineering Interview Q&A (with Examples, Easy Explanations)

---

## 1. AWS Core Services – Basics

### What is AWS? What are the benefits of using AWS?
- **AWS (Amazon Web Services)** is a cloud platform with 200+ services (compute, storage, database, etc.).
- **Benefits:** Pay-as-you-go, scalable, secure, global, no need to manage hardware.

---

### Difference between EC2, S3, RDS, Lambda?
- **EC2:** Virtual servers (“VMs”) to run any software.
- **S3:** Object storage for files/data (images, logs, backups, etc.).
- **RDS:** Managed relational databases (MySQL, PostgreSQL, etc.).
- **Lambda:** Run code without servers (“serverless”) triggered by events.

---

### Explain regions and availability zones in AWS.
- **Region:** A separate geographic location (e.g., us-east-1).
- **Availability Zone (AZ):** One or more datacenters in a region. Used for redundancy.

---

### What is IAM? How do you manage roles and permissions?
- **IAM (Identity and Access Management):** Controls who can do what in AWS.
- **Roles:** Used for apps/services, not users.
- **Permissions:** Set using policies (allow/deny actions on resources).

---

### What is the shared responsibility model in AWS?
- **AWS:** Manages the cloud (hardware, infra, security of cloud).
- **You:** Manage your data, apps, user permissions (security in the cloud).

---

## 2. AWS S3 (Simple Storage Service) 🔥

### What is S3? Use cases?
- **S3:** Scalable object storage for files.
- **Use cases:** Backups, static website hosting, log/data storage, ML data lakes.

---

### How do you store and retrieve files from S3 using Boto3 or PySpark?
**Boto3 (Python):**
```python
import boto3
s3 = boto3.client('s3')
# Upload
s3.upload_file('local.txt', 'my-bucket', 'folder/file.txt')
# Download
s3.download_file('my-bucket', 'folder/file.txt', 'local.txt')
```
**PySpark:**
```python
df = spark.read.csv('s3a://my-bucket/data.csv')
df.write.parquet('s3a://my-bucket/out/')
```

---

### Difference between S3 Standard, IA, and Glacier?
- **Standard:** Frequent access, fast, more expensive.
- **IA (Infrequent Access):** Cheaper, for less-used data.
- **Glacier:** Archival, super cheap, slow retrieval.

---

### What are pre-signed URLs? How are they used?
- **Pre-signed URL:** Temporary link to upload/download S3 file without making bucket public.
```python
url = s3.generate_presigned_url('get_object', Params={'Bucket': 'my-bucket', 'Key': 'file.txt'}, ExpiresIn=600)
```

---

### What are S3 events and how can they trigger Lambda?
- S3 can send events (e.g., new file uploaded) to trigger a Lambda function for processing.

---

## 3. AWS IAM (Identity and Access Management)

### Difference between IAM user, group, role, and policy?
- **User:** Individual identity (person/app).
- **Group:** Collection of users (assign same permissions).
- **Role:** Temporary permissions for AWS resources (used by apps/services).
- **Policy:** Document defining permissions (what actions allowed/denied).

---

### How do you give read-only access to a user for a specific S3 bucket?
- Attach a policy to the user:
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

---

### What is the principle of least privilege?
- Give users **only** the permissions they need—nothing more.

---

## 4. AWS Glue (ETL + Catalog) 🔥🔥

### What is AWS Glue? What components does it have?
- **AWS Glue:** Managed ETL (Extract-Transform-Load) service.
- **Components:** Jobs (run code), Crawlers (discover schema), Data Catalog (metadata), Triggers (schedule jobs).

---

### Difference between Glue Job, Glue Crawler, and Glue Catalog.
- **Job:** Runs ETL scripts (Python/Spark).
- **Crawler:** Scans data in S3, infers schema, updates Catalog.
- **Catalog:** Stores metadata (table definitions).

---

### How do you create ETL pipelines using Glue?
1. Use a **Crawler** to catalog data in S3.
2. Create a **Job** to transform/clean data.
3. Output to S3, Redshift, RDS, etc.

---

### What are Glue DynamicFrames vs DataFrames?
- **DynamicFrame:** More flexible, supports semi-structured data, easier to handle schema changes.
- **DataFrame:** Standard Spark DataFrame, faster but less flexible.

---

### How do you connect Glue with S3, Redshift, or RDS?
- Specify connections when creating a Job or Crawler, or use JDBC for RDS/Redshift.

---

## 5. AWS Lambda

### What is AWS Lambda? Use cases?
- **Lambda:** Run code in response to events, no server management.
- **Use cases:** Image processing, file conversion, data pipeline triggers, notifications.

---

### How do you trigger Lambda using S3 or Glue?
- S3: Set up bucket event notification (e.g., for new files).
- Glue: Set trigger after a job completes.

---

### What is the maximum execution time for Lambda?
- **15 minutes** per invocation.

---

### How do you monitor Lambda executions?
- Use **CloudWatch Logs** (view logs, set up alarms on errors, etc.).

---

## 6. AWS Redshift

### What is Amazon Redshift? How is it different from RDS?
- **Redshift:** Data warehouse for analytics (columnar storage, suited for big data SQL queries).
- **RDS:** Managed relational DB for OLTP (row-based, transactional workloads).

---

### How do you load data into Redshift from S3?
- Use the `COPY` command:
```sql
COPY my_table FROM 's3://bucket/data.csv'
CREDENTIALS 'aws_access_key_id=...;aws_secret_access_key=...'
CSV;
```

---

### What is Redshift Spectrum?
- Lets you query data directly in S3 using Redshift SQL—no need to load it into Redshift first.

---

### What is the use of COPY command in Redshift?
- Fastest way to bulk load data from S3 (or DynamoDB, etc.) into Redshift tables.

---

## 7. AWS Athena

### What is AWS Athena? When to use it?
- **Athena:** Serverless, interactive SQL queries on S3 data.
- **Use cases:** Quick analysis, ad-hoc queries, no server setup.

---

### How do you query S3 data using Athena?
1. Define a table pointing to S3 data (using Glue Catalog).
2. Run SQL queries directly in Athena Console or via SDK.

---

### Pros and cons of using Athena?
- **Pros:** Serverless, auto-scales, pay-per-query, quick setup.
- **Cons:** Slower for very large data, not for heavy ETL.

---

## 8. AWS EC2 & VPC

### What is EC2? How do you launch and connect to an instance?
- **EC2:** Virtual servers (VMs).
- Launch via AWS Console/CLI, connect using SSH:
```bash
ssh -i my-key.pem ec2-user@<public-ip>
```

---

### Difference between public and private subnets?
- **Public subnet:** Has route to internet (via Internet Gateway).
- **Private subnet:** No direct internet access (for secure backend resources).

---

### What is a VPC? What are its components?
- **VPC (Virtual Private Cloud):** Isolated network in AWS.
- **Components:** Subnets, route tables, gateways, security groups, network ACLs.

---

### What is the role of a security group and network ACL?
- **Security Group:** Firewall for EC2 instances (controls inbound/outbound traffic).
- **Network ACL:** Firewall for subnets (stateless, controls traffic at subnet level).

---

## 9. AWS RDS & Aurora

### What is RDS? How does it differ from Redshift?
- **RDS:** Managed relational database (OLTP use cases).
- **Redshift:** Data warehouse for analytics (OLAP use cases).

---

### What engines are supported by RDS?
- MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Amazon Aurora.

---

### How do you connect RDS to Glue or Lambda?
- Use JDBC connection in Glue Jobs.
- Lambda: Use DB driver in code, connect via endpoint + credentials.

---

### Difference between Multi-AZ and Read Replica?
- **Multi-AZ:** High availability (auto failover, standby copy).
- **Read Replica:** For scaling reads (no failover, async replication).

---

## 10. Monitoring & Security

### What is CloudWatch? What metrics can you monitor?
- **CloudWatch:** Monitoring and logging service.
- **Metrics:** CPU, memory, disk, network, custom app logs.

---

### What is CloudTrail and how is it different from CloudWatch?
- **CloudTrail:** Logs **API calls** (who did what in AWS).
- **CloudWatch:** Logs system and app metrics.

---

### How do you secure an S3 bucket?
- Use **bucket policies** to restrict access.
- Block public access.
- Use IAM roles for least privilege.

---

### What is KMS and how do you use it for encryption?
- **KMS (Key Management Service):** Manage encryption keys.
- Enable S3 bucket/server-side encryption with KMS keys.

---

## 11. Data Engineering Scenarios

### Design a data pipeline using S3 → Glue → Redshift
1. **Raw data** lands in S3.
2. **Glue Crawler** detects and catalogs data.
3. **Glue Job** cleans/transforms data, writes to S3 (processed).
4. **Redshift COPY** loads into warehouse for BI/analytics.

---

### How would you handle schema evolution in S3 files using Glue?
- Use Glue DynamicFrames (handle changing columns).
- Re-run the crawler to update Catalog schema.

---

### How do you schedule a job to run daily at 7 PM?
- Use Glue **Trigger** (scheduled) or **CloudWatch Events**.

---

### You have millions of JSON logs in S3 — how do you process and store insights in Redshift?
1. Use **Athena** or **Glue Job** to process logs.
2. Transform/aggregate data.
3. Write results to S3, then load into Redshift using `COPY`.

---

## 12. AWS Data Lake Design (Architecture)

### What is a Data Lake? How do you build one on AWS?
- **Data Lake:** Centralized storage for all raw/unstructured/structured data.
- **On AWS:** S3 (storage), Glue (catalog), Athena/Redshift (query), Lake Formation (security).

---

### What AWS services help in building a serverless data lake?
- S3, Glue, Lake Formation, Athena, Lambda, Step Functions.

---

### Difference between a Data Lake and Data Warehouse
- **Data Lake:** Stores all data types, flexible schema, cheap.
- **Data Warehouse:** Structured, optimized for analytics, more expensive.

---

## 13. Cost Optimization + Best Practices

### How do you reduce AWS Glue costs?
- Use smaller worker types.
- Delete unused jobs/crawlers.
- Process only necessary data (partitioning).

---

### How do you optimize S3 storage cost?
- Use S3 Lifecycle rules (move old data to IA/Glacier).
- Delete unused files.

---

### What tools help in monitoring AWS usage and cost?
- **AWS Cost Explorer**
- **AWS Budgets**
- **Trusted Advisor**

---

## 14. Miscellaneous

### Difference between EMR and Glue
- **EMR:** Managed Hadoop/Spark cluster (full control, big data processing).
- **Glue:** Serverless ETL service (no cluster management).

---

### What are AWS Step Functions?
- **Step Functions:** Orchestrate workflows (chain Lambda, Glue, etc. with error handling).

---

### What is the difference between on-demand and spot instances?
- **On-demand:** Pay per use, always available.
- **Spot:** Spare capacity, much cheaper, can be interrupted anytime.

---

## 🔧 Hands-On Tasks

### Read data from S3 in PySpark and transform it.
```python
df = spark.read.csv('s3a://my-bucket/data.csv')
df2 = df.filter(df.age > 30)
df2.write.parquet('s3a://my-bucket/processed/')
```

---

### Set up a Glue crawler to catalog Parquet files.
1. Create a Crawler in Glue.
2. Set S3 location to your Parquet files.
3. Set output database/catalog.
4. Run crawler — tables created!

---

### Trigger a Lambda when a new CSV is uploaded to S3.
- Set S3 bucket event notification (for `.csv` files) to trigger your Lambda function.

---

### Use Athena to query JSON logs in S3.
1. In Athena: Create table with JSON serde.
2. Query with SQL:
```sql
SELECT user_id, action FROM logs WHERE event='login';
```

---

### Export data from RDS to S3 using Data Pipeline or Glue.
- Use **AWS Data Pipeline** or **Glue Job** with JDBC connection to extract data from RDS and write to S3 as CSV/Parquet.

---

**Good luck! Review hands-on tasks and AWS documentation for each service.**