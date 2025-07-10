# PySpark Interview Questions & Answers (With Examples)

---

## 1. PySpark Fundamentals

### **Q1. What is PySpark? How is it different from Apache Spark?**
**Answer:**
- **PySpark** is the Python API for Apache Spark, allowing Python developers to harness the power of Spark for big data processing.
- **Apache Spark** is the core engine, written in Scala/Java, supporting APIs in Scala, Java, Python (PySpark), and R.
- **Difference**: PySpark allows you to code in Python, but the computations are executed on the Spark engine, not in the Python process.

---

### **Q2. Explain the Spark architecture (Driver, Executors, Cluster Manager).**
**Answer:**
- **Driver**: Orchestrates the Spark job, converts code into tasks, and distributes them to executors.
- **Executors**: Run on worker nodes, execute tasks, and store data in memory or disk.
- **Cluster Manager**: Manages resources (like YARN, Mesos, Kubernetes, or Spark Standalone).

**Diagram:**
```
User Code (PySpark)
      |
    Driver
      |
  Cluster Manager
  /          \
Executor   Executor
```

---

### **Q3. What are RDDs, DataFrames, and Datasets in PySpark?**
**Answer:**
- **RDD (Resilient Distributed Dataset)**: Low-level, distributed collection of objects with functional APIs (map, filter).
- **DataFrame**: Higher-level, tabular data structure with schema, similar to pandas/DataFrame or SQL table.
- **Dataset**: Strongly-typed collection of objects (available in Scala/Java; not supported in PySpark).

---

### **Q4. Difference between DataFrame and RDD in PySpark?**
| Feature        | RDD                        | DataFrame                         |
|----------------|---------------------------|-----------------------------------|
| Abstraction    | Low-level                 | High-level                        |
| Optimization   | No built-in optimization  | Catalyst Optimizer applied        |
| API            | Functional (map, filter)  | SQL-like (select, filter, groupBy)|
| Use-cases      | Complex transformations   | Most analytics tasks              |

---

### **Q5. What is lazy evaluation in Spark?**
**Answer:**
- Spark builds a logical plan for transformations (like `map`, `filter`) but does not execute them immediately.
- Execution occurs only when an action (like `count()`, `collect()`, `show()`) is called.
- **Benefit**: Optimizes execution plan for efficiency.

---

### **Q6. How does Spark handle fault tolerance?**
**Answer:**
- Spark tracks the lineage of transformations to rebuild lost data (using RDD DAG).
- If a node fails, Spark can reconstruct lost partitions using original data and transformation steps.

---

## 2. DataFrame Operations

### **Q1. How to read CSV/Parquet/JSON files in PySpark?**
```python
df_csv = spark.read.csv("data.csv", header=True, inferSchema=True)
df_parquet = spark.read.parquet("data.parquet")
df_json = spark.read.json("data.json")
```

---

### **Q2. How to perform filtering and grouping in PySpark?**
```python
# Filtering
df.filter(df.age > 21).show()

# Grouping
df.groupBy("department").count().show()
```

---

### **Q3. How to create a DataFrame from a list or dictionary?**
```python
# From list of tuples
data = [("Alice", 30), ("Bob", 25)]
df = spark.createDataFrame(data, ["name", "age"])

# From list of dicts
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
df = spark.createDataFrame(data)
```

---

### **Q4. Explain the use of select(), withColumn(), drop(), filter(), and distinct().**
- `select("col1", "col2")`: Selects specific columns.
- `withColumn("new_col", expr)`: Adds or replaces a column.
- `drop("col")`: Removes a column.
- `filter(condition)`: Filters rows.
- `distinct()`: Removes duplicate rows.

---

### **Column Operations**

#### **Q1. How to create new columns using withColumn()?**
```python
from pyspark.sql.functions import col
df.withColumn("age_plus_5", col("age") + 5).show()
```

#### **Q2. How to cast data types in PySpark?**
```python
df.withColumn("age_str", col("age").cast("string"))
```

#### **Q3. How to handle null values in DataFrames?**
```python
df.na.drop()               # Drop rows with nulls
df.na.fill({"age": 0})     # Replace nulls in 'age' with 0
df.na.replace("NULL", None)
```

---

## 3. SQL + PySpark SQL

### **Q1. How to register a DataFrame as a temporary view?**
```python
df.createOrReplaceTempView("my_table")
```

### **Q2. How do you run SQL queries on DataFrames?**
```python
spark.sql("SELECT * FROM my_table WHERE age > 21").show()
```

### **Q3. Difference between createOrReplaceTempView and createGlobalTempView.**
- `createOrReplaceTempView`: View is session-scoped.
- `createGlobalTempView`: View is global, accessible across sessions (use `global_temp.<view_name>`).

---

## 4. PySpark Joins

### **Q1. Types of joins in PySpark?**
- `inner`, `left`, `right`, `outer`, `left_semi`, `left_anti`

```python
df1.join(df2, "id", "left").show()
```

### **Q2. How do you perform broadcast join?**
```python
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), "id").show()
```

### **Q3. When to use broadcast joins vs shuffle joins?**
- **Broadcast join**: When one table is small enough to fit in memory.
- **Shuffle join**: For large tables; involves data movement (shuffle).

---

## 5. PySpark Aggregations & Grouping

### **Q1. How to do groupBy and aggregation?**
```python
df.groupBy("department").agg({"salary": "max", "age": "avg"}).show()
```

### **Q2. Explain the use of agg() with examples.**
```python
from pyspark.sql import functions as F
df.groupBy("dept").agg(F.max("salary"), F.avg("age"))
```

### **Q3. How to calculate multiple aggregations on different columns?**
```python
df.groupBy("dept").agg(
    F.max("salary").alias("max_salary"),
    F.avg("age").alias("avg_age")
)
```

---

## 6. PySpark Window Functions 🔥

### **Q1. What are window functions in PySpark?**
- Functions that perform calculations across a set of rows related to the current row (e.g., running totals, rankings).

### **Q2. Use case of row_number(), rank(), dense_rank().**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank

windowSpec = Window.partitionBy("dept").orderBy(F.desc("salary"))
df.withColumn("rank", rank().over(windowSpec))
```

### **Q3. Difference between partitionBy() and orderBy() in window specs.**
- `partitionBy()`: Splits data into groups (like SQL PARTITION BY).
- `orderBy()`: Defines order of rows within each partition.

### **Q4. How to calculate running totals or lag/lead?**
```python
from pyspark.sql.functions import sum, lag

windowSpec = Window.partitionBy("dept").orderBy("date").rowsBetween(Window.unboundedPreceding, 0)
df.withColumn("running_total", sum("sales").over(windowSpec))

df.withColumn("prev_sales", lag("sales", 1).over(windowSpec))
```

---

## 7. UDFs and Performance

### **Q1. What are UDFs (User Defined Functions) in PySpark?**
- Custom Python functions registered to extend Spark SQL functions.

### **Q2. When should UDFs be avoided?**
- UDFs are slower because they break Spark’s optimization and serialization.
- Avoid when possible; prefer built-in functions for performance.

### **Q3. How to write a Python function and use it as a UDF?**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

def double(x): return x * 2
double_udf = udf(double, IntegerType())

df.withColumn("double_age", double_udf(df.age))
```

### **Q4. Alternatives to UDFs (use built-in functions)**
- Use PySpark SQL functions (`pyspark.sql.functions`) like `when`, `col`, `regexp_replace`, `split`, etc.

---

## 8. PySpark Performance Optimization

### **Q1. What is Catalyst Optimizer?**
- Spark's query optimizer for DataFrames/Datasets that generates efficient execution plans.

### **Q2. What is Tungsten Engine?**
- Spark’s execution engine for memory management and code generation, increasing speed and efficiency.

### **Q3. How to optimize Spark jobs?**
- Partitioning, caching, using broadcast joins, avoiding shuffles, tuning executor/memory settings.

### **Q4. Difference between cache() and persist()?**
- `cache()`: Stores DataFrame in memory.
- `persist()`: Can choose storage level (memory, disk, both).

```python
df.cache()
df.persist(StorageLevel.DISK_ONLY)
```

---

## 9. PySpark File Formats and Partitioning

### **Q1. Difference between file formats: CSV, JSON, Parquet, ORC.**
- **CSV**: Simple text, no schema, slow.
- **JSON**: Semi-structured, supports nested data.
- **Parquet/ORC**: Columnar, compressed, efficient for big data.

### **Q2. How to write partitioned data using PySpark?**
```python
df.write.partitionBy("year", "month").parquet("output_path")
```

### **Q3. What is the benefit of partitioning and bucketing?**
- **Partitioning**: Faster queries by reading only relevant partitions.
- **Bucketing**: Distributes data into fixed buckets for efficient joins.

---

## 10. Error Handling & Debugging

### **Q1. Common errors in PySpark and how to resolve them?**
- **Task not serializable**: Function references non-serializable object; use only serializable objects.
- **Schema mismatch**: Fix column names/types.
- **Out of memory**: Tune memory, use partitioning.

### **Q2. How to handle schema mismatch?**
- Provide explicit schema when reading data:
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
schema = StructType([StructField("name", StringType()), StructField("age", IntegerType())])
df = spark.read.schema(schema).csv("data.csv")
```

### **Q3. What is the meaning of "Task not serializable" error?**
- Occurs when you reference objects in your driver code that can’t be serialized to the executors.

---

## 11. Real-time Case-Based Questions

### **Q1. You have a CSV with missing/null values — how will you clean and transform it?**
```python
df = spark.read.csv("file.csv", header=True, inferSchema=True)
df_clean = df.na.drop()  # or df.na.fill({"age": 0})
```

### **Q2. How would you remove duplicates based on composite keys?**
```python
df.dropDuplicates(["col1", "col2"])
```

### **Q3. A table has timestamped events — how do you get the first and last event for each user?**
```python
from pyspark.sql.functions import min, max
df.groupBy("user_id").agg(min("event_time"), max("event_time"))
```

---

## 12. Integration + Deployment

### **Q1. How do you run PySpark code on Databricks / EMR / Airflow?**
- **Databricks**: Upload notebook, attach to cluster, run.
- **EMR**: Submit as spark-submit job.
- **Airflow**: Use `SparkSubmitOperator` to schedule PySpark scripts.

### **Q2. How do you schedule and monitor PySpark jobs?**
- Use Airflow, Oozie, or built-in cluster schedulers.
- Monitor via Spark UI, logs, or external tools.

### **Q3. How would you integrate PySpark with S3, Hive, or PostgreSQL?**
```python
# S3
df = spark.read.csv("s3a://bucket/data.csv")

# Hive
spark.sql("SELECT * FROM hive_table")

# PostgreSQL
df.write.format("jdbc").option("url", "jdbc:postgresql://host/db")...
```

---

## 13. Coding Questions / Hands-on

### **Q1. Read a CSV and filter rows where column A > 100 and column B != 'XYZ'.**
```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df_filtered = df.filter((df.A > 100) & (df.B != 'XYZ'))
```

### **Q2. Find top 3 highest-paid employees per department.**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

windowSpec = Window.partitionBy("dept").orderBy(df.salary.desc())
df.withColumn("rank", row_number().over(windowSpec)).filter("rank <= 3")
```

### **Q3. Parse JSON column and extract nested fields.**
```python
from pyspark.sql.functions import from_json, col
json_schema = ...
df.withColumn("json_data", from_json(col("json_col"), json_schema))
```

### **Q4. Explode an array column and aggregate values.**
```python
from pyspark.sql.functions import explode
df_exploded = df.select("id", explode("array_col").alias("item"))
df_exploded.groupBy("item").count()
```

---

## 14. PySpark Interview Tips

- **Mention lazy evaluation** and the difference between transformations (lazy) and actions (triggers execution).
- **Discuss performance tuning:** partitioning, caching, broadcast joins.
- **Use window functions** like `partitionBy` and `orderBy` for analytics.
- **Explain real-life use cases**: integrating with S3, Airflow, Hive, SQL, etc.

---

**Good luck! Practice with real code and Spark UI for best results.**