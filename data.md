# Data Engineering Interview Q&A Guide

This guide covers essential SQL, PySpark, AWS, Databricks, and scenario-based interview questions and answers for Data Engineer roles (2+ years of experience).

---

## ✅ SQL

### 1. What is normalization?
Normalization is the process of organizing data to reduce redundancy and improve data integrity. It breaks down large tables into smaller, related ones.

**Forms of Normalization:**
- **1NF:** Atomic columns (no repeating groups).
- **2NF:** 1NF + no partial dependency.
- **3NF:** 2NF + no transitive dependency.

---

### 2. Key Types with Examples
- **Primary Key:** Unique and non-null (e.g., `EmployeeID`).
- **Foreign Key:** Refers to the primary key in another table.
- **Candidate Key:** Any field that can be a primary key.
- **Composite Key:** A combination of columns as a key.

```sql
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  CustomerID INT,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
```

---

### 3. WHERE vs HAVING
- **WHERE:** Filters rows before aggregation.
- **HAVING:** Filters after aggregation.

---

### 4. Types of JOINs
- **INNER JOIN:** Common records
- **LEFT JOIN:** All from left + matching from right
- **RIGHT JOIN:** All from right + matching from left
- **FULL JOIN:** All records from both
- **CROSS JOIN:** Cartesian product

---

### 5. Second Highest / Nth Highest Salary
```sql
-- Second Highest
SELECT MAX(Salary) FROM Employee WHERE Salary < (SELECT MAX(Salary) FROM Employee);

-- Nth Highest (e.g., 3rd)
SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC LIMIT 1 OFFSET 2;
```

---

### 6. Find Duplicates
```sql
SELECT col1, COUNT(*) FROM table GROUP BY col1 HAVING COUNT(*) > 1;
```

### 7. Delete Duplicates
```sql
DELETE FROM table WHERE rowid NOT IN (
  SELECT MIN(rowid) FROM table GROUP BY col1, col2
);
```

---

### 8. Window Functions: Use Cases
- **RANK:** Allows gaps
- **DENSE_RANK:** No gaps
- **ROW_NUMBER:** Unique sequence

---

### 9. Top 3 Departments by Avg Salary
```sql
SELECT Department, AVG(Salary) AS avg_sal
FROM Employee
GROUP BY Department
ORDER BY avg_sal DESC
LIMIT 3;
```

---

### 10. Month-over-Month Growth
```sql
SELECT
  Month,
  Sales,
  LAG(Sales) OVER (ORDER BY Month) AS Prev_Month_Sales,
  ((Sales - LAG(Sales) OVER (ORDER BY Month)) / LAG(Sales) OVER (ORDER BY Month)) * 100 AS Growth_Percent
FROM Sales;
```

---

### 11. UNION vs UNION ALL
- **UNION:** Removes duplicates.
- **UNION ALL:** Keeps duplicates.

---

### 12. GROUP BY vs PARTITION BY
- **GROUP BY:** Aggregates across groups.
- **PARTITION BY:** Divides data for window functions.

---

### 13. Indexing: Clustered vs Non-clustered
- **Clustered:** Alters row order in table (1/table).
- **Non-clustered:** Separate structure (many/table).

---

### 14. Subqueries & Correlated Subqueries
```sql
SELECT name FROM Employee e WHERE salary > (SELECT AVG(salary) FROM Employee WHERE department = e.department);
```

---

### 15. Query Optimization
- Use indexes
- Avoid `SELECT *`
- Use WHERE, LIMIT
- Use JOINs wisely

---

### 16. Pivot Operation
Use `CASE` or built-in `PIVOT` (in SQL Server/Oracle).
```sql
SELECT emp_id,
  MAX(CASE WHEN quarter = 'Q1' THEN revenue END) AS Q1,
  MAX(CASE WHEN quarter = 'Q2' THEN revenue END) AS Q2
FROM sales
GROUP BY emp_id;
```

---

### 17. DELETE vs TRUNCATE vs DROP
- **DELETE:** Row-wise deletion, can rollback.
- **TRUNCATE:** Fast removal, cannot rollback.
- **DROP:** Deletes table schema + data.

---

### 18. Update Column Using Another Table
```sql
UPDATE A SET A.salary = B.salary FROM A JOIN B ON A.id = B.id;
```

---

## ✅ PySpark

### 1. RDD vs DataFrame vs Dataset
- **RDD:** Low-level, no schema.
- **DataFrame:** High-level, tabular.
- **Dataset:** Strongly typed (Scala/Java only).

---

### 2. Create DataFrame
```python
df = spark.read.csv("file.csv", header=True)
df = spark.read.json("file.json")
df = spark.read.parquet("file.parquet")
```

---

### 3. Read/Write to S3
```python
df.write.parquet("s3a://bucket/output")
df = spark.read.json("s3a://bucket/input")
```

---

### 4. Transformations vs Actions
- **Transformations:** `map`, `filter`, `select`
- **Actions:** `count`, `collect`, `show`

---

### 5. PySpark App Flow
Input → Transformations → Actions → Output

---

### 6. Null Handling
```python
df.dropna()
df.fillna({'col': 0})
```

---

### 7. Broadcast Variables
Used to prevent data shuffle during joins with small tables.
```python
broadcast_df = broadcast(small_df)
```

---

### 8. Minimizing Shuffling
- Broadcast join
- Repartition by key
- Avoid wide transformations

---

### 9. Lazy Evaluation
Transformations are not executed until an action is called.

---

### 10. Caching & Persistence
```python
df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)
```

---

### 11. GroupBy + Aggregation
```python
df.groupBy("col").agg(sum("sales"), avg("salary"))
```

---

### 12. Join
```python
df1.join(df2, "id", "inner")
```

---

### 13. Repartition vs Coalesce
- **Repartition:** Increases partitions.
- **Coalesce:** Decreases partitions (no shuffle).

---

### 14. map vs flatMap vs mapPartitions
- **map:** Element-wise
- **flatMap:** Flattens after mapping
- **mapPartitions:** Operates on partitions

---

### 15. Schema Evolution
Use `mergeSchema=True` for reading; Delta Lake supports it natively.

---

### 16. Error Handling
Use `try-except`, custom logging, and error tracking per stage.

---

### 17. UDF Example
```python
@udf
def to_upper(s): return s.upper()
df.withColumn("name_upper", to_upper(df.name))
```

---

### 18. Catalyst Optimizer
Optimizes logical/physical execution plans automatically.

---

## ✅ AWS

### 1. AWS Glue
Serverless ETL service; runs Spark jobs.

### 2. S3 Optimization
- Use prefixes
- Enable versioning
- Use lifecycle policies

### 3. Redshift vs RDS vs DynamoDB
- **Redshift:** OLAP, columnar store
- **RDS:** Relational
- **DynamoDB:** NoSQL, key-value

### 4. ETL Scheduling
Use Glue Workflows, Lambda + CloudWatch Events, Step Functions.

### 5. IAM
Defines user/resource permissions via roles/policies.

### 6. EC2 in Pipelines
Used for self-managed Spark or Airflow.

### 7. Monitoring
Use **CloudWatch**, **Cost Explorer**, **Budgets**.

### 8. VPC
Isolated cloud network for secure deployment.

### 9. Fault-tolerant Pipelines
Use SQS + Lambda retries, EMR with spot node fallback.

### 10. Lambda in Pipelines
Used for triggers, validation, alerts.

### 11. Kinesis
- **Streams:** Real-time data
- **Firehose:** Load to S3/Redshift

### 12. CloudWatch
Monitors logs, triggers alerts, visualizes metrics.

### 13. Data Security
Use encryption (KMS), IAM roles, bucket policies.

### 14. Scaling
Use Auto Scaling Groups, EMR scaling, Lambda concurrency.

### 15. Glacier vs S3
- **S3 Standard:** Frequent access
- **Glacier:** Archival, cheaper, slower retrieval

---

## ✅ Databricks & Spark Advanced

### 1. Databricks vs Open-source Spark
Databricks offers managed Spark + notebook UI + integrations.

### 2. Delta Lake
Supports ACID, time travel, schema enforcement.

### 3. Schema Enforcement/Evolution
Use Delta with constraints + `mergeSchema`.

### 4. Jobs & Workflows
Schedule notebooks with dependencies via Workflows.

### 5. Notebook Collaboration
Use Git integrations, cell-level comments.

### 6. Partitioning Best Practices
Partition by high-cardinality column + size-based.

### 7. Debugging Long Jobs
Use Spark UI, logs, metrics, data sampling.

### 8. Managed vs Unmanaged Tables
- **Managed:** Databricks controls data lifecycle
- **Unmanaged:** External data location

### 9. Streaming Analytics
Use `readStream`, trigger intervals, sink to Delta/S3.

### 10. MLflow
Track models, metrics, and deployments in ML lifecycle.

### 11. AWS Integrations
Use IAM roles, mount S3, write to Redshift via JDBC.

### 12. Secrets Handling
Use Databricks Secrets CLI or Secret Scopes securely.

---

## ✅ Coding & Scenarios

### 1. Join Multiple DataFrames → Parquet
```python
result = df1.join(df2, "id").join(df3, "id")
result.write.parquet("/output/path")
```

### 2. Moving Average (SQL + PySpark)
```sql
SELECT id, AVG(salary) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) FROM emp;
```
```python
df.withColumn("mov_avg", avg("sales").over(Window.orderBy("date").rowsBetween(-2, 0)))
```

### 3. Corrupted File Handling
- Use try-catch
- Validate schema
- Skip or log bad records using `badRecordsPath`

### 4. End-to-End Pipeline
S3 → Glue Job → Transform → Load to Redshift → Monitor via CloudWatch

### 5. Slow Job Optimization
- Analyzed stages via Spark UI
- Broadcast join instead of shuffle
- Repartitioned data

### 6. Deduplication Logic
```sql
DELETE FROM emp WHERE rowid NOT IN (SELECT MIN(rowid) FROM emp GROUP BY id);
```
```python
df.dropDuplicates(["id"])
```

### 7. Retry Failed Records
Capture failed rows → Store in S3 → Retry job with filter.

### 8. Lineage + Audit Trail
Track job metadata, use Delta Lake history + custom logs.

---

## ✅ Behavioral

### 1. Process Improvement Example
Optimized ETL logic → 60% time savings → Reduced cost.

### 2. Cross-functional Experience
Worked with analysts to define data contracts and transformations.

### 3. Pipeline Prioritization
Impact-based priority → SLAs → Root cause → Mitigation.

### 4. Tough Decision Example
Chose schema refactoring mid-release → Fixed bugs early.

### 5. Tech Learning
Follow blogs (AWS, Databricks), attend meetups, hands-on labs.

# 📘 Data Engineer Interview Q&A Guide (Focused Compilation)

This markdown file includes a selected set of high-frequency and practical interview questions for Data Engineers, covering SQL, PySpark, AWS, and Databricks.

---

## ✅ SQL Interview Questions

### 1. How do you find the second-highest salary from a table?
```sql
SELECT MAX(salary) 
FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);
```

---

### 2. Explain the difference between INNER JOIN and LEFT JOIN
- **INNER JOIN** returns only the matching rows from both tables.
- **LEFT JOIN** returns all rows from the left table and matching rows from the right table; NULL if no match.

```sql
SELECT e.name, d.name 
FROM employee e 
INNER JOIN department d ON e.dept_id = d.id;

SELECT e.name, d.name 
FROM employee e 
LEFT JOIN department d ON e.dept_id = d.id;
```

---

### 3. How do you handle NULL values in SQL?
- Use `IS NULL` / `IS NOT NULL` to filter.
- Use `COALESCE()` to replace nulls.
- Use `IFNULL()` or `CASE WHEN` for conditional logic.

```sql
SELECT name, COALESCE(salary, 0) AS salary FROM employee;
```

---

## ✅ PySpark Interview Questions

### 4. What’s the difference between RDD and DataFrame in PySpark?
- **RDD (Resilient Distributed Dataset):** Low-level API with no schema.
- **DataFrame:** High-level API, optimized execution via Catalyst, schema-aware.

Use RDD for fine-grained transformations, DataFrame for better performance and cleaner syntax.

---

### 5. How do you handle missing values in a PySpark DataFrame?
```python
df.na.drop()                          # Drop rows with nulls
df.na.fill({"age": 0, "city": "NA"})  # Fill nulls with values
```

---

### 6. What is partitioning in Spark and why is it important?
Partitioning splits data across multiple nodes for parallel processing.

Types:
- **Hash Partitioning** (default)
- **Range Partitioning**

Optimization tips:
- Repartition large datasets
- Avoid skewed keys

```python
df.repartition("region")
df.coalesce(4)
```

---

### 7. How would you optimize a slow PySpark job?
- Use **broadcast joins** for small lookup tables.
- **Avoid wide transformations** (like groupByKey).
- **Cache intermediate results** if reused.
- **Repartition** wisely to avoid skew.
- **Read/write with optimized formats** (e.g., Parquet).

---

## ✅ AWS Interview Questions

### 8. What is Amazon S3 and how is it used in data engineering?
Amazon S3 is an object storage service.
- Used for staging, backups, ETL inputs/outputs.
- Integrated with Glue, Athena, EMR, Redshift.
- Can be optimized via prefixes, partitioning, and lifecycle policies.

---

### 9. EC2 vs EMR
- **EC2:** Raw compute resources, you manage everything.
- **EMR:** Managed Hadoop/Spark cluster service for big data workloads.

Use **EMR** for distributed ETL, **EC2** for custom compute pipelines.

---

### 10. How would you design a data pipeline using AWS services?
**S3 → Glue → Transform → Redshift → CloudWatch (Monitoring)**
- S3 for raw data
- Glue for crawling & ETL
- Redshift for analytics
- CloudWatch for alerts & logs

---

## ✅ Databricks Interview Questions

### 11. What is Databricks and how does it relate to Spark?
Databricks is a unified analytics platform built on Apache Spark.
- Offers collaborative notebooks
- Simplifies Spark job management
- Supports Delta Lake for ACID tables

---

### 12. How do you create a cluster in Databricks?
- Navigate to **Compute > Create Cluster**
- Choose runtime, node type, autoscaling
- Click **Create** to launch cluster

Clusters can be shared among notebooks or scheduled jobs.

---

# 📘 Data Engineer Interview Q&A Guide (Focused Compilation)

This markdown file includes a selected set of high-frequency and practical interview questions for Data Engineers, covering SQL, PySpark, AWS, and Databricks.

---

## ✅ SQL Interview Questions

### 1. What are ACID properties in databases?
ACID stands for:
- **Atomicity**: All operations in a transaction complete successfully or none do.
- **Consistency**: A transaction brings the database from one valid state to another.
- **Isolation**: Transactions are securely and independently processed.
- **Durability**: Once a transaction is committed, it remains so even after system failure.

---

### 2. How do you find the second-highest salary from a table?
```sql
SELECT MAX(salary) 
FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);
```

---

### 3. Write a SQL query to find the third-highest salary.
```sql
SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET 2;
```

---

### 4. Explain the different types of SQL JOINs with examples.
- **INNER JOIN**: Only matching records from both tables.
- **LEFT JOIN**: All rows from the left, matched rows from the right.
- **RIGHT JOIN**: All rows from the right, matched rows from the left.
- **FULL OUTER JOIN**: All rows from both tables; matched where possible.

**Example (INNER JOIN)**:
```sql
SELECT a.id, a.name, b.salary 
FROM employee a 
INNER JOIN payroll b ON a.id = b.emp_id;
```

---

### 5. What is a window function? Provide a use case.
Window functions perform calculations across rows related to the current row, without collapsing them.

**Example**: Ranking employees within departments:
```sql
SELECT name, department, RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS rank
FROM employee;
```

---

### 6. How do you find duplicate records in SQL?
```sql
SELECT column1, COUNT(*) 
FROM table 
GROUP BY column1 
HAVING COUNT(*) > 1;
```

---

### 7. How do you handle NULL values in SQL?
- Use `IS NULL` / `IS NOT NULL` to filter.
- Use `COALESCE()` to replace nulls.
- Use `IFNULL()` or `CASE WHEN` for conditional logic.

```sql
SELECT name, COALESCE(salary, 0) AS salary FROM employee;
```

---

## ✅ PySpark Interview Questions

### 8. What’s the difference between RDD and DataFrame in PySpark?
- **RDD (Resilient Distributed Dataset):** Low-level API with no schema.
- **DataFrame:** High-level API, optimized execution via Catalyst, schema-aware.

Use RDD for fine-grained transformations, DataFrame for better performance and cleaner syntax.

---

### 9. How do you read a CSV file with headers into a PySpark DataFrame?
```python
df = spark.read.csv('path/to/file.csv', header=True, inferSchema=True)
```

---

### 10. How can you drop duplicate rows in PySpark based on specific columns?
```python
df = df.dropDuplicates(['column1', 'column2'])
```

---

### 11. What is a broadcast join and when should you use it?
Broadcast join distributes the smaller DataFrame to all worker nodes to avoid shuffling.
Best used when one table is small enough to fit in memory.

---

### 12. How to cache a DataFrame in PySpark and why?
```python
df.cache()
```
Caching stores data in memory to improve performance during repeated actions on the same DataFrame.

---

### 13. What is partitioning in Spark and why is it important?
Partitioning splits data across multiple nodes for parallel processing.

Types:
- **Hash Partitioning** (default)
- **Range Partitioning**

Optimization tips:
- Repartition large datasets
- Avoid skewed keys

```python
df.repartition("region")
df.coalesce(4)
```

---

### 14. How would you optimize a slow PySpark job?
- Use **broadcast joins** for small lookup tables.
- **Avoid wide transformations** (like groupByKey).
- **Cache intermediate results** if reused.
- **Repartition** wisely to avoid skew.
- **Read/write with optimized formats** (e.g., Parquet).

---

## ✅ AWS Interview Questions

### 15. What is AWS Glue?
AWS Glue is a serverless ETL service that supports job scheduling, schema inference, and integrations with S3, Redshift, Athena, and more.

---

### 16. How is data stored and accessed in S3?
- Data is stored as objects in buckets.
- Accessed using unique object keys via APIs, SDKs, CLI.
- Supports versioning and lifecycle policies.

---

### 17. How would you implement a fault-tolerant ETL pipeline in AWS?
- Use S3 for raw data staging
- Glue for ETL
- CloudWatch for monitoring
- Lambda/Step Functions for retries
- Ensure cross-region backups

---

### 18. Explain IAM and its use in securing resources.
AWS IAM (Identity and Access Management):
- Controls access via users, roles, and policies
- Ensures fine-grained control over services and resources

---

### 19. What is AWS Lambda and how could you use it in data pipelines?
Lambda allows serverless compute to run code on events.
Use it for:
- Lightweight ETL
- Triggering pipelines
- Notifications/alerts in workflows

---

## ✅ Databricks Interview Questions

### 20. What is Databricks and how does it differ from running Spark on EC2?
Databricks is a managed collaborative Spark platform with:
- Notebook UI
- Cluster management
- Optimized runtimes
- Delta Lake integration

---

### 21. What is Delta Lake and why use it?
Delta Lake provides:
- ACID transactions
- Schema enforcement and evolution
- Scalable metadata
- Time travel queries

---

### 22. How do you schedule ETL pipelines in Databricks?
Use **Databricks Jobs**:
- Schedule notebooks/scripts
- Pass parameters
- Set retries and alerts

---

### 23. How do you manage credentials securely in Databricks?
Use **secret scopes** to store sensitive data like keys/passwords and access them securely in jobs.

---

### 24. Provide PySpark code to upsert (merge) data in Delta Lake.
```python
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/delta/events")
deltaTable.alias("tgt").merge(
    source_df.alias("src"),
    "tgt.id = src.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

---

## ✅ Scenario-Based & Behavioral Questions

### 25. Describe your approach to building a robust pipeline for daily sales aggregation from raw logs to dashboard reporting.
- Ingest raw logs from S3
- Transform/cleanse using PySpark or Glue
- Aggregate by store/date
- Load into Redshift or Delta Lake
- Schedule with Airflow/Databricks Jobs
- Monitor via CloudWatch

---

### 26. How do you handle sudden spikes in data volume?
- Scale compute (EMR, Databricks autoscale)
- Optimize partitioning
- Use spot instances for cost control
- Monitor with CloudWatch

---

### 27. What steps do you take to ensure data quality and integrity?
- Schema validation
- Data profiling
- Null and duplicate checks
- Logging and alerting
- Data Quality frameworks (e.g., Deequ, Great Expectations)

---

### 28. Tell me about a challenging data pipeline you designed—what technical difficulties did you face and how did you overcome them?
Structure your story:
- **Context**: What was the business need?
- **Challenge**: Corrupt data, schema drift, volume surge?
- **Actions**: Custom validation, schema evolution tools, retries
- **Results**: Improved reliability, reduced job failures, better SLAs

---

### 29. What are your favorite tools and why?
**Example:**
- **PySpark** for large-scale transformations
- **AWS Glue** for ETL orchestration
- **Databricks** for collaboration and notebook-driven development
- **Delta Lake** for data reliability

---

> **Prepared by:** Rahul Chavan  
> **Role:** Data Engineer (2+ YOE)  
> **Focus Areas:** SQL | PySpark | AWS | Databricks | ETL
