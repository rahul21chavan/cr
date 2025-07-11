# Data Engineering Interview Q&A – Simple Answers & Examples

---

## 𝗦𝗤𝗟 & 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲 𝗤𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀

**1. Top 3 highest salaries query**
```sql
SELECT salary FROM employee ORDER BY salary DESC LIMIT 3;
```

**2. Clustered vs Non-clustered Index**
- **Clustered**: Data rows are stored in order of index; only one per table. Example: Primary key.
- **Non-clustered**: Index points to actual data rows; multiple allowed. Example: Index on "email" column.

**3. Window Functions**
- Allow calculations over rows related to current row.
```sql
SELECT name, salary, RANK() OVER (ORDER BY salary DESC) FROM employee;
```

**4. Query Optimization**
- Add indexes, avoid SELECT *, filter early, analyze query plan, partition tables.

**5. Find Duplicates**
```sql
SELECT column1, COUNT(*) FROM table GROUP BY column1 HAVING COUNT(*) > 1;
```

**6. Handling NULLs**
- Use `IS NULL`, `IS NOT NULL`, `COALESCE(column, default)`, handle in logic.

**7. DELETE vs TRUNCATE vs DROP**
- **DELETE**: Removes rows, can use WHERE, logs each row.
- **TRUNCATE**: Removes all rows, no WHERE, faster, can't rollback.
- **DROP**: Deletes whole table and its structure.

**8. CTE vs Subquery**
- **CTE**: Temporary result set, improves readability.
```sql
WITH high_salary AS (SELECT * FROM employee WHERE salary > 50000)
SELECT * FROM high_salary;
```
- **Subquery**: Query inside query; less readable for complex logic.

**9. Running Total of Sales per Month**
```sql
SELECT month, sales, SUM(sales) OVER (ORDER BY month) AS running_total FROM sales_data;
```

**10. JOIN Types**
- **INNER**: Only matching rows.
- **LEFT**: All left, matched right.
- **FULL OUTER**: All rows, matched where possible.

---

## 𝗣𝘆𝘁𝗵𝗼𝗻 & 𝗗𝗮𝘁𝗮 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴

**11. Data Cleaning/Transformation (Python)**
```python
import pandas as pd
df = pd.read_csv("data.csv")
df.dropna(subset=["age"], inplace=True)
df["age"] = df["age"].astype(int)
```

**12. Python: Connect & Fetch SQL**
```python
import sqlite3
conn = sqlite3.connect('test.db')
df = pd.read_sql_query("SELECT * FROM employee", conn)
```

**13. Pandas vs PySpark**
- **Pandas**: In-memory, best for small data.
- **PySpark**: Distributed, handles big data across clusters.

**14. Exception Handling (ETL)**
```python
try:
    run_etl_job()
except Exception as e:
    print(f"Error: {e}")
```

**15. Data Processing Libraries**
- Pandas, NumPy, PySpark, Dask, SQLAlchemy, Openpyxl.

---

## 𝗖𝗹𝗼𝘂𝗱 & 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲

**16. Cloud Data Warehouse Architecture**
- **Snowflake/BigQuery**: Separate compute and storage; scalable; access via SQL; stores data in cloud (S3, GCS).

**17. OLAP vs OLTP**
- **OLAP**: Analytics, complex queries, large volumes.
- **OLTP**: Fast transactions, simple queries, real-time.

**18. Data Quality in ETL**
- Validate formats, check for nulls, deduplicate, use frameworks like Great Expectations.

**19. Apache Kafka Role**
- Real-time data streaming, decouples producers/consumers, buffers data flow between systems.

**20. What is ETL?**
- **Extract**: Get data from sources.
- **Transform**: Clean, convert.
- **Load**: Store in target (DB, data warehouse).
- **Tools**: Glue, Airflow, Talend, Informatica.

**21. Project Flow & Architecture**
- Ingest data → Clean/transform → Store → Analyze/report. Use pipelines, orchestration tools, automation.

**22. Default Spark File Format**
- **Parquet** (columnar, compressed, fast for analytics).

**23. Why Parquet in Spark?**
- Efficient storage, compression, faster queries (reads only needed columns).

**24. Optimization Techniques**
- Caching, partitioning, use broadcast joins, filter early, avoid shuffles, tune memory.

**25. groupByKey vs reduceByKey**
- **groupByKey**: Groups all values, more shuffle, less efficient.
- **reduceByKey**: Reduces locally before shuffling, more efficient.

**26. Rack Awareness in Hadoop**
- Distributes data blocks across racks for fault tolerance.

**27. Common File Formats**
- Parquet, Avro, CSV, JSON, ORC.

**28. Spark Fault Tolerance**
- Uses lineage, re-computes lost data using RDD transformations.

**29. Ignore Nulls When Loading**
- `df.dropna()` in PySpark or Pandas.

**30. Find 3rd Highest Salary**
```sql
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk FROM employee
) WHERE rnk = 3;
```

**31. Convert Positives to Negatives (PySpark)**
```python
df.withColumn("invoice", when(df.invoice > 0, -df.invoice).otherwise(df.invoice))
```

**32. Date "20/04/1963" to Integer**
```python
from datetime import datetime
int(datetime.strptime("20/04/1963", "%d/%m/%Y").strftime("%Y%m%d"))
```

**33. Extract "ML", "GM", "LTR" in Spark**
```python
from pyspark.sql.functions import col
df.filter(col("value").isin(["ML","GM","LTR"]))
```

**34. Data Modeling Questions**
- Normalization, denormalization, SCD, surrogate keys, star/snowflake schema.

---

## PySpark Focus

**35. DataFrame vs RDD**
- **RDD**: Low-level, functional, more code.
- **DataFrame**: Tabular, optimized, SQL-like, easier.

**36. PySpark Optimization**
- Cache, repartition, broadcast joins, filter early, avoid collect(), tune resources.

**37. Catalyst Optimizer**
- Optimizes query plans for faster execution (reorders, combines, prunes).

**38. Serialization Formats**
- **Parquet**: Columnar, analytics.
- **Avro**: Row, streaming.
- Chosen for speed, compression, schema support.

**39. Skewed Data Problems**
- Repartition, salt keys, use broadcast joins, filter hot keys.

**40. Memory Management**
- Executors have memory limits; cache/persist, spill to disk if needed.

**41. PySpark Join Types**
- Inner, left, right, full, semi, anti.
  - *Example*: `df1.join(df2, "id", "left")`

**42. broadcast() Function**
- Use when joining large and small datasets; copies small dataset to all nodes.

**43. UDFs in PySpark**
```python
from pyspark.sql.functions import udf
def my_func(x): return x*2
spark.udf.register("my_func", my_func)
```

**44. Lazy Evaluation**
- Transformations are not run until an action (count, collect) is called; helps optimize jobs.

**45. Create DataFrame**
```python
data = [(1,"A"),(2,"B")]
df = spark.createDataFrame(data, ["id","name"])
```

**46. RDD Concept**
- Immutable distributed collection; supports parallel ops (map, filter).

**47. Actions vs Transformations**
- **Action**: Runs job, returns value (collect, count).
- **Transformation**: Builds lineage (map, filter).

**48. Null Handling in DataFrames**
- `df.dropna()`, `df.fillna(value)`

**49. Partition in PySpark**
- Splits data for parallelism. Use `repartition()` and `coalesce()` to control.

**50. Narrow vs Wide Transformation**
- **Narrow**: Data stays in partition (map).
- **Wide**: Requires shuffle (groupBy).

**51. Schema Inference**
- PySpark guesses schema from input data; may need to specify for accuracy.

**52. SparkContext Role**
- Entry point; manages resources, job scheduling.

**53. Aggregations in PySpark**
```python
df.groupBy("col").agg({"sales":"sum"})
```

**54. Caching Strategies**
- Use `df.cache()` for repeated use, or `persist()` for custom storage levels.

---

_Each answer provides a direct example or explanation for interview revision!_