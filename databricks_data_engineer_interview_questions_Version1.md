# Data Engineer Interview Questions (2 Years Experience) – Databricks Focus

## 1. What is Databricks and how does it differ from Apache Spark?

**Answer:**  
Databricks is a cloud-based platform built on top of Apache Spark that provides a collaborative workspace for data engineering, machine learning, and analytics. It simplifies Spark cluster management, integrates with cloud storage, provides a notebook interface, and offers features like Delta Lake for ACID transactions.

- **Key differences:**  
    - **Managed Environment:** Databricks automates cluster setup and management.
    - **Collaborative Workspace:** Notebooks, dashboards, commenting.
    - **Delta Lake:** ACID transactions, schema enforcement, time travel.
    - **Integrated Workflows:** Jobs, ML integrations, REST APIs.

---

## 2. Explain the ETL process in Databricks with a real-time example.

**Answer:**  
ETL stands for Extract, Transform, Load. In Databricks, you typically use Spark DataFrames or SQL for ETL.

**Example:**  
Suppose you need to ingest sales data from Azure Blob, clean and transform it, and store it in a Delta table.

- **Extract:**  
    ```python
    df = spark.read.csv("wasbs://container@storageaccount.blob.core.windows.net/sales_data.csv", header=True)
    ```

- **Transform:**  
    ```python
    from pyspark.sql.functions import col, to_date
    df_clean = df.withColumn("sales_date", to_date(col("sales_date"), "yyyy-MM-dd")) \
                 .filter(col("amount") > 0)
    ```

- **Load:**  
    ```python
    df_clean.write.format("delta").mode("overwrite").save("/mnt/delta/sales")
    ```

- **Real-world scenario:**  
    - You set up a Databricks Job to run this ETL pipeline daily.
    - You perform incremental loads using MERGE for upserts.

---

## 3. How do you implement incremental data loads in Databricks using Delta Lake?

**Answer:**  
Incremental loads bring in only new or updated data. In Delta Lake, you use `MERGE` statements for upserts.

**Example:**  
Assuming `updates_df` contains new/changed records:

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/mnt/delta/sales")

delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

- **Scenario:**  
    - Streaming data from Kafka, batch updates from source systems.
    - Use `_change_tracking` columns or timestamps for identifying changes.

---

## 4. How do you handle schema evolution in Delta Lake?

**Answer:**  
Delta Lake supports schema evolution, allowing you to add new columns.

**Example:**  
If new data has additional columns, use:

```python
df.write.format("delta").option("mergeSchema", "true").mode("append").save("/mnt/delta/sales")
```

- **Scenario:**  
    - Upstream source adds a new column.
    - Delta Lake merges schema automatically.

---

## 5. What is time travel in Delta Lake and how is it useful?

**Answer:**  
Time travel lets you query previous versions of a Delta table.

**Example:**  
To query the table as it was 5 versions ago:

```python
df_old = spark.read.format("delta").option("versionAsOf", 5).load("/mnt/delta/sales")
```

- **Scenario:**  
    - Restore accidentally deleted data.
    - Audit historical changes for compliance.

---

## 6. How do you orchestrate ETL workflows in Databricks?

**Answer:**  
Use Databricks Jobs to schedule notebooks, JARs, or Python scripts.

- **Example pipeline:**  
    - Step 1: Extract from Blob Storage.
    - Step 2: Transform & clean.
    - Step 3: Load to Delta Lake.
    - Step 4: Notify via REST API.

- **Features:**  
    - Job clusters (ephemeral clusters per job run).
    - Dependency management (job steps).
    - Monitoring and alerting.

---

## 7. How do you manage and optimize Spark jobs in Databricks?

**Answer:**  
- **Partitioning:** Repartition DataFrames for parallelism.
- **Caching:** Use `.cache()` for iterative algorithms.
- **Broadcast joins:** For small lookup tables.
- **Cluster configuration:** Choose appropriate node types and autoscaling.
- **Monitoring:** Use Spark UI, Databricks Job metrics.

**Example:**  
```python
df.repartition(20).write.format("delta").save("/mnt/delta/optimized_sales")
```

---

## 8. How do you ingest real-time streaming data in Databricks?

**Answer:**  
Databricks supports Structured Streaming.

**Example:**  
Ingest from Kafka:

```python
df_stream = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "server:9092")
    .option("subscribe", "sales_topic")
    .load())

df_parsed = df_stream.selectExpr("CAST(value AS STRING)")
```

- **Scenario:**  
    - Real-time fraud detection.
    - Dashboarding with low latency.

---

## 9. How do you handle data quality and validation in ETL pipelines?

**Answer:**  
- **Validation checks:** Null values, data types, ranges.
- **Expectation libraries:** Use tools like Deequ, Great Expectations, or custom code.
- **Example:**  
    ```python
    invalid_df = df.filter(col("amount").isNull() | (col("amount") < 0))
    if invalid_df.count() > 0:
        # Log or send alert
    ```

---

## 10. How do you implement error handling and logging in Databricks notebooks?

**Answer:**  
- **Try/except blocks:** Capture errors.
- **Databricks REST API:** Send logs/alerts.
- **Example:**  
    ```python
    try:
        # ETL code
    except Exception as e:
        print(f"Error: {e}")
        # Optionally write to a log table
    ```

---

## 11. What are Delta Lake Z-ORDER and OPTIMIZE, and when should you use them?

**Answer:**  
- **OPTIMIZE:** Compacts small files into larger files.
- **Z-ORDER:** Co-locates related data for faster queries on specific columns.

**Example:**  
```sql
OPTIMIZE sales_table ZORDER BY (customer_id)
```

- **Scenario:**  
    - Large datasets with queries filtered by specific columns (customer_id, date).
    - Improves query performance significantly.

---

## 12. How do you secure data in Databricks?

**Answer:**  
- **ACLs:** Folder-level access controls.
- **Table Access Control (Table ACLs):** Grant/revoke permissions.
- **Data encryption:** Storage-level (Azure, AWS) and in-transit.
- **Row-level security:** Implement using views or filters.

---

## 13. How do you manage dependencies in Databricks workflows?

**Answer:**  
- **Libraries:** Attach Python/Scala packages to clusters.
- **Cluster-scoped libraries:** Use `.whl` or `.jar` files.
- **Notebook dependencies:** Use `%pip install` or `%conda install`.

---

## 14. How do you integrate Databricks with external data sources?

**Answer:**  
- **Cloud storage:** Azure Blob, AWS S3 via mount points.
- **RDBMS:** JDBC connections to SQL Server, MySQL, etc.
- **REST APIs:** Python/Scala requests from notebooks.

**Example:**  
```python
jdbc_url = "jdbc:sqlserver://server.database.windows.net:1433;database=Sales"
df = spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "sales").load()
```

---

## 15. How do you ensure ETL job reliability and monitor failures?

**Answer:**  
- **Retries:** Configure job retries in Databricks Jobs.
- **Alerts:** Set up email or webhook alerts on failures.
- **Logging:** Write logs to Delta tables or cloud storage.
- **Monitoring:** Use Databricks Job UI, cluster logs.

---

## 16. How do you optimize data storage and cost in Databricks?

**Answer:**  
- **Partitioning:** Partition tables by date or key columns.
- **OPTIMIZE:** Reduce small files for efficient storage.
- **Vacuum:** Remove old data files.
- **Data skipping:** Store data in Parquet/Delta for predicate pushdown.

---

## 17. How do you handle slowly changing dimensions (SCD) in Databricks?

**Answer:**  
- **SCD Type 1:** Overwrite existing values.
- **SCD Type 2:** Add new rows for changes, keep history.

**Example SCD2:**
```python
from pyspark.sql.functions import current_timestamp

new_df = updates_df.withColumn("effective_date", current_timestamp())
delta_table.alias("target").merge(
    new_df.alias("source"),
    "target.id = source.id AND target.current = true"
).whenMatchedUpdate(set={"current": "false"}).whenNotMatchedInsert(values={"current": "true"}).execute()
```

---

## 18. What is Medallion Architecture in Databricks?

**Answer:**  
A layered approach to data pipelines:

- **Bronze:** Raw data
- **Silver:** Cleaned/enriched data
- **Gold:** Aggregated business-level data

**Scenario:**  
- Ingest to Bronze Delta tables from source.
- Transform and cleanse to Silver.
- Aggregate for reporting in Gold.

---

## 19. How do you implement CDC (Change Data Capture) in Databricks?

**Answer:**  
- Use source system CDC logs.
- Use Delta Lake's MERGE for upserts.
- Use streaming pipelines for near real-time CDC.

**Example:**  
- Ingest Kafka CDC topic.
- Parse and upsert into Delta Lake.

---

## 20. How do you troubleshoot a slow Spark job in Databricks?

**Answer:**  
- Check Spark UI (stages, tasks, shuffles).
- Unbalanced partitions.
- Skewed data.
- Insufficient cluster resources.
- Large shuffles or joins.
- Optimize with partitioning, broadcast joins, increasing executor memory.

---

## 21. What are common pitfalls in Databricks ETL pipelines and how to avoid them?

**Answer:**  
- **Small files problem:** Use OPTIMIZE.
- **Schema drift:** Use `mergeSchema`.
- **Data skew:** Repartition, use salting.
- **Unmanaged dependencies:** Use cluster libraries.
- **Failure to monitor:** Set up alerts and logging.

---

## 22. How do you automate testing of data pipelines in Databricks?

**Answer:**  
- Use unit tests (PyTest, ScalaTest).
- Data validation checks.
- Automated notebook jobs with assertions.
- Test environments (dev/stage/prod).

---

## 23. How do you version and deploy Databricks notebooks?

**Answer:**  
- Store notebooks in Git repositories.
- Use Databricks Repos for Git integration.
- Deploy via Jobs or REST API.

---

## 24. How do you scale Databricks jobs for large data volumes?

**Answer:**  
- Use autoscaling clusters.
- Partition input data.
- Optimize transformations.
- Use Delta Lake for scalable storage.

---

## 25. How do you migrate data from on-premises to Databricks?

**Answer:**  
- Use cloud storage as staging (Azure/AWS).
- Use Databricks notebooks for ingestion.
- Validate and transform using ETL pipelines.

---

## 26. Give a real-time example of troubleshooting data corruption in a Delta table.

**Answer:**  
**Scenario:**  
- A job accidentally overwrote Gold table with incorrect data.

**Resolution:**
- Use Delta Lake time travel to restore to previous version.
    ```python
    df_restore = spark.read.format("delta").option("versionAsOf", old_version).load("/mnt/delta/gold")
    df_restore.write.format("delta").mode("overwrite").save("/mnt/delta/gold")
    ```
- Audit logs for root cause.

---

## 27. How do you schedule and monitor streaming ETL jobs in Databricks?

**Answer:**  
- Use Databricks Jobs for continuous streaming jobs.
- Monitor via Job UI, cluster logs.
- Use `awaitTermination()` in streaming notebooks.

---

## 28. How do you handle GDPR or data privacy requirements in Databricks?

**Answer:**  
- Encrypt sensitive data.
- Mask or anonymize PII in ETL.
- Use Delta Lake `VACUUM` to delete old versions.
- Control access with ACLs.

---

## 29. How do you handle schema drift in incoming data?

**Answer:**  
- Use `mergeSchema` in Delta Lake.
- Profile incoming data for new columns.
- Automate schema updates in ETL.

---

## 30. How do you integrate Databricks with BI tools?

**Answer:**  
- Expose Delta tables to Power BI, Tableau via JDBC/ODBC.
- Use Databricks SQL endpoints.
- Schedule ETL to update reporting tables.

---

**Note:**  
These questions and answers aim to cover a broad spectrum of scenarios you are likely to encounter as a Data Engineer with 2 years of experience working on Databricks. Real-world examples are provided wherever possible. You can further elaborate or customize these based on your project experience.
