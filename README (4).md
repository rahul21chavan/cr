# Python Fundamentals for Data Engineers: Detailed Guide & Examples

Welcome to your comprehensive Python reference! This document covers foundational Python concepts, syntax, and common patterns that every data engineer should know. Each section includes detailed explanations and practical code examples suitable for real-world data engineering tasks.

---

## 1. Print Statements

Python's `print()` function is used to display output. You can print strings, variables, and use formatting arguments.

```python
print("hello", 1, "euu")  # Simple print
print("hello", 1, "euu", sep='@')  # Custom separator
print("hello rahul. How is your day?\nhii?\nhow is ur day")  # Newlines
print('hello ''ansh'' how are you')  # Adjacent string literals
print("hello \'ansh\' hi")  # Escaping quotes
```

**Explanation:**  
- `sep` controls the separator between arguments.
- `\n` creates a new line.
- You can concatenate strings by writing them next to each other or using `+`.

---

## 2. Variables & Operations

Variables store data. Python supports dynamic typing.

```python
my_var = 'rahul'
my_lname = 'chavan'
x = 10
y = 5

print(my_var, x + y, y - x)  # Operations in print
print(my_var + my_lname)  # String concatenation
print(my_var + " " + my_lname)  # Adding a space
```

**Explanation:**  
- Variables can hold strings, numbers, etc.
- Arithmetic and string operations are intuitive.

---

## 3. Multiple Assignment

Python allows multiple variables to be assigned in a single line.

```python
x, y, z = 10, 5, 20
my_var = 'rahul'  # Comment: my name
```

**Explanation:**  
- Useful for unpacking tuples/lists.

---

## 4. Comments

Use `#` for single-line comments, `''' ... '''` or `""" ... """` for multi-line comments.

```python
my_var = 'rahul'  # This is my name
'''
This is a
multi-line comment
'''
```

---

## 5. Mathematical Approaches

Python supports different ways to write mathematical expressions.

```python
total = 10+20+30+20+10
print(total)

total = 10+20+\
        30+20+10
print(total)

total = (10+20+
        30+20+10)
print(total)
```

---

## 6. Indentation and Blocks

Indentation defines code blocks in Python.

```python
x = 1
if x == 1:  # Parent Block
    print('wow')  # Child Block
print("wooo")  # Outside block
```

---

## 7. Typecasting

Explicit and implicit type conversions.

```python
a = 10
b = "10"

print(type(a))
b_new = int(b)
a_new = str(a)
print(type(a_new))
print(type(b_new))

a = 10
b = 10.5
print(type(a))
print(a + b)  # Implicit conversion to float
```

---

## 8. String Indexing & Slicing

Strings are sequences of characters, indexed from 0.

```python
x = "AnshLamba"
print(x[1])  # n
print(x[-1])  # a
print(x[2:4])  # sh
print(x[0:4])  # Ansh
print(x[:])  # Full string
print(x[0:len(x)])  # Full string
```

---

## 9. String Methods

Useful built-in methods for string manipulation.

```python
x = "Ansh Lamba"
print(x.lower())
print(x.upper())
print(x.replace("h", "z"))
print(x.replace("sh", "z"))
```

---

## 10. File Operations

Check file extensions and names.

```python
file = "raw_data.csv"
if file.endswith(".csv"):
    print("csv_file")
if file.startswith("raw"):
    print("raw file")
```

---

## 11. Useful String Methods

```python
statement = "hello hi rahul is rahul here"
print(statement.count("rahul"))  # Count occurrences

demo_str = "Hello"
print(demo_str.isnumeric())  # False

demo_var = "10"
demo_al = "10abc"
print(demo_var.isnumeric())  # True
print(demo_al.isalnum())  # True
```

---

## 12. Conditionals

Basic and nested if/else statements.

```python
x = 11
if x == 10:
    print("true")
else:
    print("false")

x = 1100
if x == 10:
    print("x is 10")
elif x > 100:
    if x > 1000:
        print("x is right")
else:
    print("x is not big")
```

---

## 13. Loops

Iterate over lists and ranges.

```python
my_list = ["order", "products", "customers"]
for i in my_list:
    print(i)

for i in range(1, 101):
    print(i)
```

### Loop with condition

```python
tbl_list = ["order", "products", "customers"]
for i in tbl_list:
    if i.lower() == "order":
        print("table order")
    else:
        print("no table")
```

### Nested Loops

```python
for i in tbl_list:
    print(i)
    for x in i:
        print(x)  # Iterates over characters
```

### While Loop

```python
x = 1
while x < 11:
    print(x)
    x += 1
```

---

## 14. Data Structures: Lists

Lists are mutable and versatile.

```python
my_list = [1, 2, "Ansh", "Lamba", ['aa', 'bb', 'cc']]
print(my_list[4][1])  # bb
print(my_list[-3:])  # ['Ansh', 'Lamba', ['aa', 'bb', 'cc']]
print(my_list[::2])  # [1, 'Ansh', ['aa', 'bb', 'cc']]

my_list.append("hero")
my_list.insert(1, "hero")
my_list.pop()
my_list.reverse()
print(my_list[::-1])
```

### List Comprehensions

```python
my_list = [1, 2, 3, 4, 5, 6]
new_list = [i * i for i in my_list]
print(new_list)

new_list = [i * i for i in my_list if i % 2 == 0]
print(new_list)
```

---

## 15. Dictionaries

Key-value pairs, mutable.

```python
my_dictionary = {"x": 1, "y": 2, "z": 3}
my_dictionary["x"] = 10
print(my_dictionary.items())
my_dictionary = {"x": 1, "y": 2, "z": 3, "demo": {"a": 1, "b": 2, "c": 3}}
print(my_dictionary['demo']['b'])
```

---

## 16. Sets

Unique, unordered collections.

```python
a = {1, 2, 3, 4, 5, 5, 5}
b = {10, 11, 3, 2, 5}
print(a.union(b))
print(a.intersection(b))
a.remove(2)
a.add(20)
print(a)
a = set()
print(type(a))  # set
```

---

## 17. Tuples

Immutable sequences.

```python
my_tup = (1, 2, 3, 4, 5)
my_tuplist = list(my_tup)
my_tuplist.append(6)
my_tup = tuple(my_tuplist)
print(my_tup)
```

---

## 18. Functions

Define reusable code blocks.

```python
def my_func():
    if x > 10:
        print("greater than 10")
    else:
        print("IDK")
my_func()
```

### Arguments, Default Values, Variable Arguments

```python
def my_func(p_x, p_y=30):
    print(p_x, p_y)
my_func(20, 60)

def my_func(*p_x):
    print(p_x)
my_func(10, 20, 40)

def my_func(**p_x):
    print(p_x)
    print(p_x.keys())
my_func(x=10, y=20, z=40)
```

### Lambda Functions

```python
addition = lambda x, y: x + y
var = addition(10, 30)
print(var)
```

### Map, Filter, Reduce

```python
from functools import reduce

my_list = [1, 2, 3, 4, 5]
def square(p_x): return p_x * p_x
result = list(map(square, my_list))
print(result)

def is_even(p_x): return p_x % 2 == 0
result = list(filter(is_even, my_list))
print(result)

def add(x, y): return x + y
result = reduce(add, my_list)
print(result)
```

---

## 19. Exception Handling

```python
x = "10"
try:
    if int(x) > 10:
        print("greater than 10")
    else:
        print("bla")
except Exception as e:
    print(e)
print("hello")
```

### Finally Block

```python
x = 10
try:
    if x > 10:
        print("greater than 10")
    else:
        print("bla")
except Exception as e:
    print(e)
finally:
    print("I will always run")
```

---

## 20. F-Strings

Efficient string formatting.

```python
name = "ansh"
my_string = f"hello my {name} is lamba"
print(my_string)
```

---

## 21. Global & Local Variables

```python
x = 100  # global

def my_func():
    global x
    x = 5  # modifies global x
    print(x)
my_func()
```

---

## 22. Raising Exceptions

```python
x = 99
if x < 100:
    raise ValueError("less than 100")
```

---

## 23. Enumerate

Efficient index-value looping.

```python
my_list = [100, 200, 300, 400, 500]
for i, x in enumerate(my_list):
    print(x)
```

---

## 24. Object-Oriented Programming (OOP)

### Basic Class

```python
class Employee:
    emp_name = "Rahul"
    emp_dept = "IT"
    def info(self):
        print(f"Employee {self.emp_name} works for {self.emp_dept}")

emp1 = Employee()
print(emp1.emp_name)
print(emp1.emp_dept)
emp1.info()
```

### Constructor, Class & Static Methods

```python
class Employee:
    company_name = 'xyz'
    def __init__(self, emp_name, emp_dept):
        self.emp_name = emp_name
        self.emp_dept = emp_dept
    def info(self):
        print(f"Employee {self.emp_name} works for {self.emp_dept} and {self.company_name}")
    @staticmethod
    def addition(x, y):
        print(x + y)
    @classmethod
    def change_company(cls, new_company):
        cls.company_name = new_company

emp1 = Employee("Priya", "IT")
emp1.info()
Employee.change_company("NewCo")
emp1.info()
```

---

### Inheritance

```python
class Company:
    def __init__(self, com_name):
        self.com_name = com_name
    def company_info(self):
        print(f"Company name is {self.com_name}")

class Employee(Company):
    def __init__(self, emp_name, com_name):
        super().__init__(com_name)
        self.emp_name = emp_name
    def emp_info(self):
        print(f"Employee Name is {self.emp_name}")
    def company_info_child(self):
        print("This is running")
        super().company_info()

emp1 = Employee("Rahul", "XYZ")
emp1.company_info_child()
```

---

### Multilevel Inheritance

```python
class Company:
    def __init__(self, com_name):
        self.com_name = com_name
    def company_info(self):
        print(f"Company name is {self.com_name}")

class Country:
    def __init__(self, country_name):
        self.country_name = country_name
    def country_info(self):
        print(f"Country name is {self.country_name}")

class Department(Company):
    def __init__(self, dept_name, com_name):
        super().__init__(com_name)
        self.dept_name = dept_name
    def department_info(self):
        print(f"The department is {self.dept_name} of {self.com_name}")

class Employee(Company, Country):
    def __init__(self, emp_name, com_name, country_name):
        Company.__init__(self, com_name)
        Country.__init__(self, country_name)
        self.emp_name = emp_name
    def full_info(self):
        print(f"Employee {self.emp_name} lives in {self.country_name}")

emp1 = Employee("Rahul", "XYZ", "India")
emp1.full_info()
```

---

## 25. Threading & Parallelism

Useful for data engineering ETL jobs.

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor

table = ["orders", "products", "customers", "reviews", "cancels"]

def my_func(i):
    wait = random.randint(1, 5)
    time.sleep(wait)
    print(f"I am {i}, I took {wait} sec")

with ThreadPoolExecutor(max_workers=len(table)) as executor:
    executor.map(my_func, table)
```

---

## 26. HTTP Requests

Used in ETL, API, and web scraping.

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()
print(data)
```

---

## 27. OS Operations

Useful for file management and automation.

```python
import os

os.makedirs("new_folder", exist_ok=True)
print(os.path.abspath(__file__))
```

---

## Additional Data Engineering Examples

### CSV Reading & Writing

```python
import csv

# Writing to CSV
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "age"])
    writer.writerow(["Rahul", 25])

# Reading from CSV
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

### Pandas for Data Engineers

```python
import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())

# Filtering data
filtered = df[df['age'] > 20]
print(filtered)
```

### Working with JSON

```python
import json

data = {'name': 'Rahul', 'age': 25}
json_str = json.dumps(data)
print(json_str)

parsed = json.loads(json_str)
print(parsed['name'])
```

---

## Conclusion

This README covers the majority of Python features and patterns you’ll encounter as a data engineer. For more advanced topics, such as distributed data processing, machine learning, or cloud integrations, consider exploring libraries like PySpark, Dask, TensorFlow, or cloud SDKs.

Feel free to extend this file and add your own examples as you learn more!

---

## Recommended Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Awesome Python for Data Engineering](https://github.com/pawamoy/awesome-python)