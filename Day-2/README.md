# Python Training – Day 2

This folder contains the Python assignments completed as part of **Day 2 of Python and Django Training**.

The tasks focus on advanced Python functions, decorators, file handling, JSON, data processing, comprehensions, lambda functions, `map()`, `filter()`, and sorting.

---

## Project Structure

```text
day_2/
│
├── employees.json
├── task_1_advanced_functions.py
├── task_2_file_handling.py
├── task_3_data_processing.py
└── README.md
```

---

# Requirements

* Python 3.x
* VS Code
* Git

No external Python packages are required for Tasks 1–3.

The following built-in Python modules are used:

```text
time
json
pathlib
```

---

# Task 1 – Advanced Functions and Decorators

### File

```text
task_1_advanced_functions.py
```

### Completed Requirements

* Created a function to accept employee details using `**kwargs`
* Created a salary statistics function using `*args`
* Calculated:

  * Total salary
  * Average salary
  * Highest salary
  * Lowest salary
* Created a closure for maintaining a running total
* Created an `execution_logger` decorator
* Calculated function execution time
* Applied the decorator to multiple functions
* Added input validation
* Added meaningful error messages
* Added type hints and docstrings

### Concepts Learned

* `*args`
* `**kwargs`
* Closures
* `nonlocal`
* Decorators
* Wrapper functions
* Type hints
* Docstrings
* Exception handling

---

# Task 2 – File Handling and JSON

### Files

```text
task_2_file_handling.py
employees.json
```

### Completed Requirements

* Created employee records
* Stored employee data in JSON
* Loaded employee data from JSON
* Saved employee data to JSON
* Displayed all employees
* Searched for employees by ID
* Added new employees
* Prevented duplicate employee IDs
* Updated employee details
* Deleted employees
* Counted total employees
* Validated employee information
* Validated salary values
* Handled missing JSON files
* Handled invalid JSON data

### Concepts Learned

* File handling
* `with open()`
* `json.load()`
* `json.dump()`
* JSON serialization
* JSON deserialization
* `pathlib.Path`
* CRUD operations
* Data validation
* Exception handling

---

# Task 3 – Data Processing

### File

```text
task_3_data_processing.py
```

### Completed Requirements

* Used list comprehension to get employee names
* Filtered employees earning more than `45,000`
* Filtered Development department employees
* Created a dictionary containing employee names and salaries
* Used `map()` to calculate yearly salaries
* Used `filter()` to find employees earning more than `50,000`
* Used `lambda` and `sorted()` to sort employees by salary
* Grouped employees by department
* Calculated average salary for each department
* Found the second-highest distinct salary
* Kept the original employee list unchanged

### Concepts Learned

* List comprehension
* Dictionary comprehension
* Lambda functions
* `map()`
* `filter()`
* `sorted()`
* Sets
* Data grouping
* Data transformation

---

# Sample Employee Data

The data used for Task 3 is:

```python
employees = [
    {
        "name": "Aman",
        "department": "Development",
        "salary": 45000
    },
    {
        "name": "Riya",
        "department": "HR",
        "salary": 38000
    },
    {
        "name": "Neha",
        "department": "Development",
        "salary": 55000
    },
    {
        "name": "Rahul",
        "department": "Testing",
        "salary": 42000
    },
    {
        "name": "Priya",
        "department": "Development",
        "salary": 60000
    }
]
```

---

# Running the Programs

Run each task individually from the terminal.

### Task 1

```bash
python task_1_advanced_functions.py
```

### Task 2

```bash
python task_2_file_handling.py
```

### Task 3

```bash
python task_3_data_processing.py
```

---

# Testing

The completed tasks were tested with normal inputs and edge cases.

### Task 1 Testing

* Valid employee details
* Empty employee details
* Invalid age input
* Negative age
* Valid salaries
* Empty salary input
* Invalid salary values
* Negative salary
* Running total with multiple values
* Decorator execution and timing

### Task 2 Testing

* Adding an employee
* Duplicate employee ID
* Searching for an existing employee
* Searching for a non-existing employee
* Updating employee information
* Deleting an employee
* Counting employees
* Empty employee data
* Missing `employees.json`
* Invalid JSON data
* Invalid salary
* Negative salary
* Data persistence after saving

### Task 3 Testing

* Empty employee list
* Salary filtering
* Department filtering
* Salary sorting
* Yearly salary calculation
* Employee grouping
* Department salary averages
* Duplicate salary values
* Second-highest distinct salary
* Confirmed that the original employee list is not modified

---

# Problems Faced

### JSON Dictionary Keys

JSON converts dictionary keys into strings when data is serialized. Employee IDs were therefore converted back to integers when loading the JSON data so that ID-based operations remained consistent.

### Input Validation

User input needed validation for empty values, invalid numbers, negative values, and invalid salary values.

### Updating Employee Data

The update functionality required handling empty input so that existing employee details could be retained.

### `map()` and `filter()`

`map()` and `filter()` return iterator objects, so their results were converted into lists when a list representation was required.

### Second-Highest Distinct Salary

Duplicate salaries had to be removed before determining the second-highest salary. A `set` was used to keep only distinct salary values.

---

# Topics Learned

During these tasks, I learned and practiced:

* Advanced functions
* Function arguments
* `*args`
* `**kwargs`
* Closures
* `nonlocal`
* Decorators
* Execution time measurement
* Type hints
* Docstrings
* Exception handling
* File handling
* JSON
* Serialization
* Deserialization
* CRUD operations
* `pathlib`
* List comprehensions
* Dictionary comprehensions
* Lambda functions
* `map()`
* `filter()`
* `sorted()`
* Sets
* Data grouping
* Data transformation
* Input validation

---

# Git

The completed work is maintained using Git and pushed to GitHub.

To view the commit history:

```bash
git log --oneline
```
