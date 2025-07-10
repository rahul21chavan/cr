# Python Interview Questions & Answers (With Examples)

---

## 1. Python Fundamentals

### Q1. What are Python’s key features?
- Easy to learn and read (simple syntax)
- Dynamically typed
- Interpreted, not compiled
- Cross-platform
- Large standard library and community
- Supports OOP, functional, and procedural paradigms

---

### Q2. Difference between a list, tuple, and set?
| Type   | Ordered | Mutable | Duplicates | Syntax        |
|--------|---------|---------|------------|---------------|
| List   | Yes     | Yes     | Yes        | `[1, 2, 3]`   |
| Tuple  | Yes     | No      | Yes        | `(1, 2, 3)`   |
| Set    | No      | Yes     | No         | `{1, 2, 3}`   |

---

### Q3. What is the difference between is and ==?
- `is` checks **identity** (same object in memory)
- `==` checks **equality** (same value/content)

---

### Q4. What are *args and **kwargs?
- `*args`: Collects extra positional arguments as a tuple
- `**kwargs`: Collects extra keyword arguments as a dictionary

```python
def demo(*args, **kwargs):
    print(args)   # tuple of positional arguments
    print(kwargs) # dict of keyword arguments
```

---

### Q5. What is the difference between shallow copy and deep copy?
- **Shallow copy**: Copies references of nested objects (`copy.copy()`)
- **Deep copy**: Copies all objects recursively (`copy.deepcopy()`)

```python
import copy
copy.copy(list)    # shallow
copy.deepcopy(list) # deep
```

---

### Q6. How is memory management handled in Python?
- Automatic garbage collection (reference counting + cyclic GC)
- Memory allocation handled by Python’s memory manager

---

## 2. Data Structures

### Q1. How would you choose between a list, dictionary, set, and tuple for data tasks?
- **List**: Ordered, allows duplicates, mutable (e.g., sequence of items)
- **Dictionary**: Key-value pairs, fast lookups, mutable (e.g., mapping names to values)
- **Set**: Unique unordered items (e.g., removing duplicates)
- **Tuple**: Ordered, immutable (e.g., fixed collections, hashable)

---

### Q2. How do you remove duplicates from a list?
```python
lst = [1, 2, 2, 3]
unique = list(set(lst))
```

---

### Q3. What is the time complexity of dictionary lookups?
- Average case: **O(1)** (hash table)
- Worst case (rare): **O(n)**

---

### Q4. How do you sort a list of tuples by the second element?
```python
lst = [(1, 3), (2, 2), (3, 1)]
sorted_lst = sorted(lst, key=lambda x: x[1])
```

---

## 3. File Handling

### Q1. How do you read/write a text file in Python?
```python
# Read
with open('file.txt', 'r') as f:
    content = f.read()

# Write
with open('file.txt', 'w') as f:
    f.write('Hello')
```

---

### Q2. How to read a large file line by line without loading all into memory?
```python
with open('large.txt') as f:
    for line in f:
        process(line)
```

---

### Q3. How do you parse a JSON or CSV file?
```python
import json, csv

# JSON
with open("file.json") as f:
    data = json.load(f)

# CSV
import pandas as pd
df = pd.read_csv("file.csv")
```

---

## 4. Functions and Scope

### Q1. What is a lambda function? How is it used?
- Anonymous, one-line function: `lambda x: x+1`
```python
add = lambda x, y: x + y
```

---

### Q2. What is the difference between map(), filter(), and reduce()?
- `map(func, seq)`: Applies function to all elements
- `filter(func, seq)`: Selects elements where function returns True
- `reduce(func, seq)`: Reduces sequence to single value (from functools import reduce)

---

### Q3. Explain local vs global variables.
- **Local**: Defined inside a function, accessible only within
- **Global**: Defined outside all functions, accessible everywhere

---

### Q4. What are decorators in Python?
- Functions that modify behavior of other functions
```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

---

## 5. Object-Oriented Programming

### Q1. What is OOP in Python? Explain concepts: class, object, inheritance, polymorphism.
- **Class**: Blueprint for objects
- **Object**: Instance of class
- **Inheritance**: Child class inherits from parent
- **Polymorphism**: Same method name behaves differently in different classes

---

### Q2. What is the difference between __init__ and __str__?
- `__init__`: Constructor, runs on object creation
- `__str__`: String representation, used by print()

---

### Q3. What is method overloading and overriding?
- **Overloading**: Same method name, different params (Python doesn’t support directly; can use default args)
- **Overriding**: Child class redefines parent’s method

---

### Q4. How does Python implement encapsulation?
- Using private variables (prefix `_` or `__`), not enforced but a convention

---

## 6. Exception Handling

### Q1. How does Python handle errors? Use of try, except, finally?
```python
try:
    # code
except ValueError:
    # handle error
finally:
    # always runs
```

---

### Q2. What’s the difference between Exception and BaseException?
- `BaseException` is the root of all exceptions (including SystemExit, KeyboardInterrupt)
- `Exception` is for user-defined and most built-in errors (excluding system-exiting ones)

---

### Q3. How to raise custom exceptions?
```python
class MyError(Exception):
    pass

raise MyError("Error Message")
```

---

## 7. Python for Data Engineering

### Q1. How do you read and process CSV/JSON/Parquet files using Pandas?
```python
import pandas as pd
df = pd.read_csv("file.csv")
df = pd.read_json("file.json")
df = pd.read_parquet("file.parquet")
```

---

### Q2. How do you connect to a SQL database using Python?
```python
import sqlalchemy
engine = sqlalchemy.create_engine("postgresql://user:pass@host/db")
df = pd.read_sql("SELECT * FROM table", engine)
```

---

### Q3. How do you automate ETL using Python scripts?
- Use schedule/cron/Airflow for scheduling
- Use pandas for data wrangling
- Use functions/modules for reusability

---

### Q4. What is the use of os, pathlib, and glob modules in file processing?
- `os`: File management, environment, paths
- `pathlib`: OOP path handling
- `glob`: Pattern-based file search

```python
from pathlib import Path
for file in Path('.').glob('*.csv'):
    print(file)
```

---

## 8. Pandas & NumPy Basics

### Q1. How do you handle missing values in Pandas?
```python
df.dropna()                      # Drop rows with NaNs
df.fillna(0)                     # Fill missing with 0
df['col'].fillna(df['col'].mean())
```

---

### Q2. Difference between loc[] and iloc[]?
- `loc[]`: Label-based indexing (e.g., df.loc[2, "name"])
- `iloc[]`: Integer position-based indexing (e.g., df.iloc[2, 0])

---

### Q3. How to group and aggregate data using Pandas?
```python
df.groupby('col').agg({'salary':'mean', 'age':'max'})
```

---

### Q4. What’s the use of apply() and lambda in Pandas?
- `apply()` applies a function to Series or DataFrame rows/columns.
- Often used with `lambda` for custom logic.

```python
df['col2'] = df['col1'].apply(lambda x: x*2)
```

---

## 9. Regex & String Manipulation 🔥

### Q1. How do you extract email IDs from a text using regex?
```python
import re
emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', text)
```

---

### Q2. How do you check if a string contains only digits?
```python
s.isdigit()
# Or with regex: re.fullmatch('\d+', s)
```

---

### Q3. Difference between re.search() and re.match()?
- `re.match()`: Checks match at start of string
- `re.search()`: Checks match anywhere in string

---

### Q4. Clean this text: remove special characters and convert to lowercase.
```python
import re
clean = re.sub(r'[^a-zA-Z0-9 ]', '', text).lower()
```

---

## 10. Modules & Packaging

### Q1. How do you structure a Python project?
```
myproject/
  mypackage/
    __init__.py
    module1.py
    module2.py
  tests/
    test_module1.py
  setup.py
  requirements.txt
  README.md
```

---

### Q2. What are virtual environments (venv, pipenv)?
- Isolated Python environments to manage dependencies per project
```bash
python -m venv venv
pipenv install
```

---

### Q3. How to create and import custom modules?
- Create `module.py`, then import as `import module` or `from module import func`

---

## 11. Iterators, Generators & Comprehensions

### Q1. What is the difference between iterator and generator?
- **Iterator**: Object with `__next__()` and `__iter__()`
- **Generator**: Uses `yield`, auto-creates iterator, keeps state

---

### Q2. Use of yield in a function?
- Makes a function a generator, can pause and resume

---

### Q3. Write a generator for Fibonacci numbers.
```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a+b
```

---

### Q4. How to use dictionary and list comprehensions effectively?
```python
squares = [x*x for x in range(5)]
dict_squares = {x: x*x for x in range(5)}
```

---

## 12. Multithreading and Multiprocessing

### Q1. What is GIL (Global Interpreter Lock) in Python?
- A mutex that allows only one thread to execute Python bytecode at a time (CPython), limiting CPU-bound threading

---

### Q2. When to use threading vs multiprocessing?
- **Threading**: I/O-bound tasks (network, file I/O)
- **Multiprocessing**: CPU-bound tasks (heavy computation)

---

### Q3. Write a multiprocessing example to speed up I/O-bound tasks.
```python
from multiprocessing import Pool

def task(x):
    # I/O operation
    return x*x

with Pool(4) as p:
    result = p.map(task, [1,2,3,4])
```

---

## 13. API Integration & Automation

### Q1. How do you make API calls using requests module?
```python
import requests
response = requests.get("https://api.github.com")
data = response.json()
```

---

### Q2. How do you handle JSON responses and headers?
```python
headers = {'Authorization': 'Bearer TOKEN'}
response = requests.get(url, headers=headers)
json_data = response.json()
```

---

### Q3. Automate a task: download files from an API and upload to S3.
```python
import requests, boto3
s3 = boto3.client('s3')
resp = requests.get(file_url)
s3.upload_fileobj(io.BytesIO(resp.content), 'bucket', 'file.txt')
```

---

## 14. Unit Testing

### Q1. How do you write test cases using unittest or pytest?
```python
import unittest

class TestMyFunc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1,2), 3)

# pytest: just write functions prefixed with test_
```

---

### Q2. What is mocking? How is mock.patch() used?
- Mocking: Replace real objects/functions with fakes during tests
```python
from unittest.mock import patch

@patch('module.func')
def test_func(mock_func):
    mock_func.return_value = 10
```

---

## 15. Real-World Coding Challenges

### Q1. Read a CSV and count rows with missing values.
```python
df = pd.read_csv('file.csv')
missing = df.isnull().any(axis=1).sum()
```

---

### Q2. Parse a nested JSON and flatten it into a DataFrame.
```python
import pandas as pd
import json
from pandas import json_normalize

with open('file.json') as f:
    data = json.load(f)
df = json_normalize(data)
```

---

### Q3. Clean and standardize name fields using regex.
```python
df['name'] = df['name'].str.replace(r'[^a-zA-Z ]', '', regex=True).str.lower()
```

---

### Q4. Write a class to manage connections to multiple databases.
```python
class DBManager:
    def __init__(self, configs):
        self.dbs = {name: self.connect(cfg) for name, cfg in configs.items()}
    def connect(self, cfg):
        # return db connection object
        pass
    def get(self, name):
        return self.dbs[name]
```

---

### Q5. Compress and archive files from a folder based on extension and date.
```python
import glob, zipfile
from datetime import datetime

files = glob.glob('*.txt')
with zipfile.ZipFile('archive.zip', 'w') as z:
    for f in files:
        # filter by date if needed
        z.write(f)
```

---

## 16. Python + PySpark Integration

### Q1. How do you submit PySpark jobs using Python scripts?
- Use `spark-submit`:
```bash
spark-submit my_script.py
```

---

### Q2. How to use SparkSession inside a Python function?
```python
from pyspark.sql import SparkSession

def my_func():
    spark = SparkSession.builder.appName("App").getOrCreate()
    # use spark...
```

---

### Q3. How do you convert a Pandas DataFrame to PySpark and vice versa?
```python
# Pandas to PySpark
import pandas as pd
from pyspark.sql import SparkSession

pandas_df = pd.DataFrame({'a': [1,2]})
spark = SparkSession.builder.getOrCreate()
spark_df = spark.createDataFrame(pandas_df)

# PySpark to Pandas
pandas_df2 = spark_df.toPandas()
```