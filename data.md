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

> **Prepared by:** Rahul Chavan  
> **Role:** Data Engineer (2+ YOE)  
> **Focus Areas:** SQL | PySpark | AWS | Databricks | ETL
