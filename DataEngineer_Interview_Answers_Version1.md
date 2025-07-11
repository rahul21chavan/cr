# Data Engineering Interview Q&A (Easy Explanations & Examples)

---

## ✅ SECTION 1: PySpark & Spark (Core Focus)

### 1. **Difference: RDD, DataFrame, Dataset in Spark**
- **RDD (Resilient Distributed Dataset)**: Low-level, immutable distributed collection of objects; functional APIs (map, reduce, filter).
  - *Example*: `rdd.map(lambda x: x + 1)`
- **DataFrame**: Tabular data (rows/columns), optimized, supports SQL queries.
  - *Example*: `df.filter(df['age'] > 21)`
- **Dataset**: Strongly-typed (Scala/Java), combines benefits of RDD/DataFrame. Python uses DataFrame.

### 2. **Spark Execution Model (Driver, Executors, DAG, Stage, Task)**
- **Driver**: Coordinates jobs, creates DAG (Directed Acyclic Graph).
- **Executors**: Run tasks on worker nodes.
- **DAG**: Logical plan of transformations.
- **Stage**: Group of tasks that can be executed together.
- **Task**: Smallest unit of execution (processes partition).

*Example*: When you run `df.groupBy('city').count()`, the Driver builds a DAG, splits work into stages/tasks, and Executors process partitions.

### 3. **Wide vs Narrow Transformation**
- **Narrow**: Data processed within partition (no shuffle).  
  - *Example*: `map`, `filter`
- **Wide**: Data moves between partitions (requires shuffle).  
  - *Example*: `groupByKey`, `join`

### 4. **Spark Data Shuffling & Optimization**
- **Shuffling**: Redistributing data across partitions (expensive).
- **Optimization**: Use `reduceByKey` over `groupByKey`, increase parallelism, filter early, avoid unnecessary shuffles.

### 5. **Broadcast Joins**
- **Broadcast Join**: Small table copied to all nodes for joining with a big table.
- *Use when*: One table is much smaller than the other.
  - *Example*: `df_big.join(broadcast(df_small), ...)`

### 6. **Handling Skewed Data in Spark Joins**
- **Skewed Data**: Some keys have much more data.
- *Solutions*: Salting keys, using broadcast joins, repartitioning, or filtering skewed keys.

### 7. **Checkpointing in Spark**
- **Checkpointing**: Persist RDD/DataFrame to reliable storage (HDFS/S3) for fault tolerance.
- *Required*: For long lineage, streaming jobs, or iterative algorithms.

### 8. **Structured Streaming vs Spark Streaming**
- **Spark Streaming**: Micro-batch, RDD-based, legacy.
- **Structured Streaming**: DataFrame-based, supports event time, windowing, watermark, SQL, more robust.

### 9. **Watermarking in Structured Streaming**
- **Watermark**: Tells engine how late data can arrive for aggregations.
  - *Example*: `withWatermark("timestamp", "10 minutes")`

### 10. **Spark File Formats; Parquet vs Avro**
- **Supported**: Parquet, ORC, Avro, JSON, CSV, Delta, Text.
- **Parquet**: Columnar, compressed, fast for analytics.
- **Avro**: Row-based, great for Kafka/streaming, supports schema evolution.

---

## ✅ SECTION 2: SQL for ETL & Analytics

### 1. **SQL: Second Highest Salary**
```sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

### 2. **CTE vs Subquery vs View**
- **CTE (WITH clause)**: Temporary named result set, readable.
- **Subquery**: Query inside another query.
- **View**: Saved query, virtual table.

### 3. **Window Functions**
- *ROW_NUMBER*:
  ```sql
  SELECT *, ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC) AS rn FROM employees
  ```
- *RANK*:
  ```sql
  SELECT *, RANK() OVER(ORDER BY salary DESC) FROM employees
  ```

### 4. **Star vs Snowflake Schema**
- **Star**: Fact table + denormalized dimension tables.
- **Snowflake**: Fact + normalized dimensions/sub-dimensions.
  - *Example*: Customer table in star has all info; in snowflake, address is a separate normalized table.

### 5. **Optimizing Slow SQL in Snowflake/Redshift**
- Partitioning, clustering, indexing
- Prune unnecessary columns
- Use result caching
- Avoid functions on indexed columns

### 6. **Join Types**
- **Inner Join**: Matching rows both tables.
- **Left Join**: All left, matched right.
- **Left Semi Join**: Only left rows with matches in right.
- **Anti Join**: Left rows with no match in right.

### 7. **Partitioning & Clustering in SQL Engines**
- **Partitioning**: Divides table into segments (by date, region).
- **Clustering**: Groups similar rows for faster search.
- Improves query performance by reducing scan.

### 8. **Materialized View vs Normal View**
- **Materialized**: Stores data, can be refreshed, faster for heavy queries.
- **View**: Virtual, always up to date, no storage.

### 9. **Surrogate vs Natural Key**
- **Natural Key**: Real-world unique value (email, SSN).
- **Surrogate Key**: Artificial (auto-increment id).
  - *Example*: `user_id` as surrogate, `email` as natural.

### 10. **SQL: LAG/LEAD for Month-over-Month Sales**
```sql
SELECT month, sales, LAG(sales) OVER(ORDER BY month) AS prev_sales
FROM sales_data
```

---

## ✅ SECTION 3: Python for Data Engineering

### 1. **Efficient Large File Processing**
- Read line by line (generator).
```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line
```

### 2. **Shallow vs Deep Copy**
- **Shallow**: Copies references.
- **Deep**: Copies all nested objects.
```python
import copy
a = [[1,2],[3,4]]
b = copy.copy(a)     # shallow
c = copy.deepcopy(a) # deep
```

### 3. **Read/Write S3 in Python**
```python
import boto3
s3 = boto3.client('s3')
s3.download_file('bucket','file.txt','local.txt')
s3.upload_file('local.txt','bucket','file.txt')
```

### 4. **Pandas: Clean & Transform**
```python
import pandas as pd
df = pd.read_csv('data.csv')
df.dropna(inplace=True)
df['age'] = df['age'].astype(int)
```

### 5. **Python Generators in ETL**
- Yield values one at a time, memory efficient for streams or big files.

### 6. **Custom Exception Handling**
```python
class DataValidationError(Exception): pass
try:
    validate(data)
except DataValidationError as e:
    log(e)
```

### 7. **List Comprehension vs map/filter**
- List comprehension is more readable, supports conditions.
```python
[x*2 for x in lst if x > 0]
list(map(lambda x: x*2, filter(lambda x: x > 0, lst)))
```

### 8. **Custom Validator for Data Quality**
```python
def is_valid(row):
    return row['age'] > 0 and '@' in row['email']
```

### 9. **Testing Strategies**
- Use `pytest` for unit tests.
- Mock external dependencies.
- Integration tests for end-to-end pipeline.

### 10. **Modularize Python Codebase**
- Organize code into packages, modules, use `__init__.py`.
- Reusable functions/classes in separate files.

---

## ✅ SECTION 4: AWS & Cloud Ecosystem

### 1. **Glue vs EMR**
- **Glue**: Serverless ETL, easy for quick jobs, managed.
- **EMR**: Custom clusters, big data processing, flexible for Spark/Hadoop.

### 2. **S3 & Storage Classes**
- **S3**: Object storage; stores files as "objects" in "buckets".
- **Classes**: Standard, Intelligent-Tiering, One Zone-IA, Glacier (archival).

### 3. **AWS Lake Formation**
- Service for building secure data lakes, manages ingestion, access, governance.

### 4. **Glue Job Types**
- **Spark**: PySpark/Scala jobs.
- **Python Shell**: Lightweight Python scripts.
- **Ray**: Distributed Python (ML/AI workloads).

### 5. **IAM Roles/Policies**
- Roles: Identities with permissions.
- Policies: JSON rules (allow/deny actions).
- Secure access by least privilege, use roles for services.

### 6. **Glue Crawlers vs Catalog Tables**
- **Crawler**: Scans data, creates/updates tables.
- **Catalog Table**: Metadata about datasets.

### 7. **Monitoring Glue Jobs**
- Use CloudWatch logs, Glue job metrics, notifications/alerts.

### 8. **Batch vs Streaming Ingestion**
- **Batch**: Periodic loads (daily files).
- **Streaming**: Real-time (Kinesis, Kafka).

### 9. **Data Masking in AWS Pipelines**
- Use Glue transformations, Lambda, or DMS to encrypt/mask PII.

### 10. **Kinesis Data Streams vs Firehose**
- **Streams**: Real-time, custom apps can process events.
- **Firehose**: Auto-loads data to S3/Redshift, managed, easy for delivery.

---

## ✅ SECTION 5: Databricks, Delta Lake & Lakehouse

### 1. **Delta Lake vs Parquet**
- **Delta Lake**: Adds ACID, versioning, upserts, time travel on top of Parquet.

### 2. **Versioning & Time Travel in Delta**
- Can query previous table versions (`VERSION AS OF`), restore data.

### 3. **Upserts (Merge) in Delta**
```sql
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```

### 4. **Unity Catalog Metadata**
- Centralized governance, manages table/database permissions.

### 5. **Databricks SQL vs Spark SQL**
- **Databricks SQL**: Managed, BI-friendly, web UI.
- **Spark SQL**: Runs within Spark, CLI/programmatic.

### 6. **Z-ordering**
- Sorts data by columns to optimize query performance, minimizes I/O.

### 7. **Bronze/Silver/Gold Layers**
- **Bronze**: Raw data.
- **Silver**: Cleaned, refined.
- **Gold**: Aggregated, analytics-ready.

### 8. **Great Expectations Integration**
- Add data checks directly in Databricks Notebooks, automate validation.

### 9. **Delta Live Tables (DLT) Benefits**
- Automated pipeline management, data quality, versioning, error handling.

### 10. **Deploy Job: Airflow/CICD**
- Use Airflow DAGs to trigger Databricks jobs via REST API.
- CICD with GitHub Actions/Azure DevOps for code, tests, deployment.

---

## ✅ SECTION 6: Orchestration, Data Modeling & DQ

### 1. **Airflow: DAGs, Tasks, Operators**
- **DAG**: Directed Acyclic Graph, defines workflow.
- **Task**: Atomic unit (PythonOperator, BashOperator).
- **Operator**: Type of task (e.g., Python, Bash, SparkSubmit).

### 2. **Ensuring Idempotency**
- Design jobs so rerunning produces same result (use upserts, overwrite, checkpoints).

### 3. **Retry Mechanism in Airflow**
- Set `retries` and `retry_delay` parameters on operators.

### 4. **Normalized vs Denormalized Models**
- **Normalized**: Avoid data duplication (many tables, joins).
- **Denormalized**: Merge tables for faster reads, some redundancy.

### 5. **Slowly Changing Dimensions (SCD) Type 1/2**
- **Type 1**: Overwrite old data (no history).
- **Type 2**: Add new row, track history (valid_from, valid_to).

### 6. **Great Expectations with Spark**
- Write expectations (rules) for Spark DataFrames, test column values, types, ranges.

### 7. **Validate Schema Evolution**
- Schema registry, automated tests, version control for schemas.

### 8. **Track Dataset Metadata**
- Use data catalog (AWS Glue, Unity Catalog), logging, documentation.

### 9. **Common Data Quality Issues**
- Nulls, duplicates, schema drift, outliers; handled via validation, cleaning, alerts.

### 10. **Testing Data Pipelines**
- Unit: Individual steps.
- Integration: End-to-end.
- Regression: After changes.

---

## ✅ SECTION 7: Streaming, DevOps & Misc.

### 1. **Kafka Integration with Spark Structured Streaming**
- Read from Kafka topic using Spark’s `readStream` API.

### 2. **Flink vs Spark Streaming**
- **Flink**: True real-time, event-time, stateful.
- **Spark**: Micro-batch, easier for batch + streaming.
- Prefer Flink for low-latency, complex event processing.

### 3. **Checkpointing in Streaming**
- Saves state to storage (HDFS/S3) for fault tolerance.

### 4. **Deploy/Monitor Spark on Kubernetes/Docker**
- Package app in Docker image, deploy as Kubernetes job/pod.
- Monitor via Spark UI, Prometheus, Grafana.

### 5. **Git & Version Control for ETL**
- Use branches, pull requests, tags for releases.
- Track code, configs, pipeline changes.

### 6. **CI/CD for Data Pipelines**
- Automate tests, linting, deployment using Jenkins, GitHub Actions, or Azure DevOps.

### 7. **Handling Sensitive Data (PII)**
- Mask/encrypt data, use IAM policies, audit logs, restrict access.

### 8. **GDPR/CCPA Compliance**
- Allow data deletion, anonymization, audit trails, consent management.

### 9. **Legacy ETL Migration Approach**
- Assess old workflows, design cloud-native equivalents, validate with parallel runs, cutover with rollback plans.

### 10. **Bonus: Recent Data Pipeline Example**
*Built a nightly ETL in Databricks for ingesting sales data, cleaning, aggregating, and loading to a Delta Lake gold table. Faced schema drift and uneven data arrival, solved with dynamic schema detection and robust error handling. Automated quality checks with Great Expectations and orchestrated jobs via Airflow for reliability.*

---

*Use these easy answers and examples for interview prep, revision, or onboarding!*