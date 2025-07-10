# AWS Data Pipeline: S3 → Glue → Redshift

## Overview

This document describes a real-world data pipeline architecture using AWS S3, AWS Glue (Crawler & Job), and Amazon Redshift for analytics and BI. The pipeline covers:
- Raw data ingestion to S3
- Metadata cataloging with Glue Crawler
- Data cleaning and transformation with Glue Job (PySpark)
- Loading processed data into Redshift using the COPY command

---

## 1. Data Ingestion: Landing Raw Data in S3

### **How Data Lands in S3**

**Scenarios:**  
- Application logs, IoT sensor data, e-commerce events, or CSV/JSON files exported nightly from transactional databases.
- Data is uploaded via:
  - AWS SDK (Boto3 for Python)
  - S3 Console (manual)
  - AWS CLI
  - Automated ETL tools or direct application integration

**Example (Python Boto3):**
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('local_data/sales_2025-07-10.csv', 'my-raw-bucket', 'sales/2025/07/10/sales.csv')
```

**Recommended S3 Structure:**
```
s3://my-raw-bucket/sales/{year}/{month}/{day}/sales.csv
s3://my-raw-bucket/logs/{year}/{month}/{day}/log.json
```
*Organizing by date and data type makes lifecycle management and partitioned reading easy.*

---

## 2. Glue Crawler: Detecting & Cataloging Data

### **Purpose**
- Scans S3 locations, infers schema and partitions, and registers tables in the Glue Data Catalog.

### **Steps**
1. **Create a Glue Crawler:**
   - Source: S3 path to raw data (e.g., `s3://my-raw-bucket/sales/`)
   - Output: Glue Database/Table (e.g., `raw_sales`)
   - Scheduling: On demand or periodic (e.g., every hour)

2. **Crawler Operation:**
   - Reads new files, infers column types, and updates the catalog table metadata.
   - Detects new partitions (e.g., new day/month folders).

### **Benefits**
- Makes S3 data queryable by Athena/Glue.
- Handles schema evolution (new columns detected).

---

## 3. Glue Job: Data Cleaning & Transformation

### **Purpose**
- Reads raw data, performs cleaning (removes nulls, fixes types, standardizes), and writes processed data back to S3.

### **Example: Common Cleaning Tasks**
- Remove rows with missing critical fields (e.g., `order_id`)
- Standardize date formats
- Trim string fields, normalize case
- Cast numeric columns to correct type
- Deduplicate records based on primary/composite keys
- Handle corrupt or malformed records

### **Sample Glue PySpark Script**
```python
import sys
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, trim, lower, to_date

# Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Read raw data from Glue Catalog table (created by Crawler)
raw_df = glueContext.create_dynamic_frame.from_catalog(
    database="raw_db",
    table_name="raw_sales"
).toDF()

# Data Cleaning/Transformation
clean_df = (
    raw_df
    # Remove rows with missing order_id
    .filter(col("order_id").isNotNull())
    # Trim and lowercase customer_name
    .withColumn("customer_name", lower(trim(col("customer_name"))))
    # Parse date
    .withColumn("sale_date", to_date(col("sale_date"), "yyyy-MM-dd"))
    # Cast sales_amount to float
    .withColumn("sales_amount", col("sales_amount").cast("float"))
    # Remove duplicates
    .dropDuplicates(["order_id"])
)

# Write to processed S3 path (partitioned by date)
clean_df.write.mode("overwrite").partitionBy("sale_date").parquet("s3://my-processed-bucket/sales_cleaned/")
```

**Common Transformations:**  
- Normalizing text (e.g., lowercasing names)
- Parsing & formatting dates
- Converting data types
- Removing or imputing nulls
- Generating new columns (e.g. extracting year/month)

---

## 4. Processed Data Cataloging (Optional)

- (Re-)Run a Glue Crawler on the processed S3 location (`s3://my-processed-bucket/sales_cleaned/`) to update schema and partitions in the Glue Catalog.
- This enables Athena/Redshift Spectrum queries on cleaned data.

---

## 5. Loading Data into Redshift

### **Purpose**
- Load transformed/cleaned data from S3 into Redshift for analytics, dashboards, and BI.

### **Steps**
1. **Create External Table (Optional, via Redshift Spectrum):**
   - Allows direct querying of S3 data from Redshift.

2. **Load Data Using COPY Command**
   - Redshift reads Parquet/CSV files from S3 and loads into internal tables.

**Example COPY Command:**
```sql
COPY sales
FROM 's3://my-processed-bucket/sales_cleaned/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftCopyRole'
FORMAT AS PARQUET;
```
- Supports parallel load for speed.
- Can specify partition filters if needed.

---

## 6. Real-World Enhancements

### **Error Handling & Monitoring**
- Use logging in Glue Jobs to track errors and data quality issues.
- Send notifications (SNS, Slack) on job failures or anomalies.

### **Scheduling & Orchestration**
- Use Glue Triggers or AWS Step Functions to automate the workflow.
- Example: Trigger Glue Job after Crawler completes, or on file arrival in S3 (via Lambda).

### **Schema Evolution**
- Glue DynamicFrames handle changes in schema (new, missing columns).
- Use versioned tables in Redshift or schema migration scripts for downstream changes.

### **Cost Optimization**
- Partition S3 data by date/key for efficient reading.
- Use S3 lifecycle rules to move old raw data to Glacier or delete.

---

## 7. Full Pipeline Diagram

```
[Data Producers]
     |
     v
[Raw Data in S3] <--- (Upload via API, CLI, apps)
     |
     v
[Glue Crawler] --(Catalogs schema)--> [Glue Data Catalog]
     |
     v
[Glue Job]
     |  (Cleans, transforms)
     v
[Processed Data in S3]
     |
     v
[Glue Crawler] (optional, catalogs processed data)
     |
     v
[Redshift COPY]
     |
     v
[Redshift Data Warehouse]
     |
     v
[BI Visualization, Dashboards]
```

---

## 8. Example: End-to-End Flow

**Scenario:**  
- Nightly, e-commerce transactions are exported as CSV to S3.
- Glue Crawler detects new files, updates schema.
- Glue Job cleans (removes duplicates, fixes columns), writes Parquet partitioned by date to S3.
- Another Crawler catalogs the processed data.
- Redshift COPY loads clean data for analytics.

---

## 9. References & Best Practices

- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Amazon Redshift COPY Docs](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)
- [Best practices for S3 data lakes](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/index.html)
- Use partitioned, columnar formats (Parquet) for analytics.
- Secure S3 buckets and Glue/Redshift IAM roles.

---

**Tip:**  
Automate the pipeline using AWS Step Functions for production workflows. Monitor each stage and validate row counts at each step for data quality.

---