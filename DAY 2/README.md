# DAY 2 - Python Training Tasks

## Overview

This folder contains the Python training tasks completed during Day 2 of the Burnett Brucke internship.

The tasks focused on advanced functions, decorators, file handling, JSON, comprehensions, lambda functions, map, filter, sorting, grouping, and data processing.

---

## Tasks Completed

### Task 1 - Advanced Functions and Decorators

Created `task_1_advanced_functions.py`.

The task included:

- Created a function that accepts employee details using `**kwargs`.
- Created a function that accepts any number of salaries using `*args`.
- Calculated:
  - Total salary
  - Average salary
  - Highest salary
  - Lowest salary
- Created a closure that maintains a running total.
- Created an `execution_logger` decorator.
- Used the decorator with at least three functions.
- Added type hints and docstrings.
- Validated empty input and invalid salary values.
- Avoided repeating the same validation logic.

### Concepts Learned

- `*args`
- `**kwargs`
- Closures
- Decorators
- Type hints
- Docstrings
- Input validation
- Code reusability

---

### Task 2 - File Handling and JSON

Created `task_2_file_handling.py` and stored employee data in `employees.json`.

The task included:

- Added employee details:
  - ID
  - Name
  - Email
  - Department
  - Salary
- Saved employee details to a JSON file.
- Read and displayed all employee details.
- Searched for an employee by ID.
- Updated employee department or salary.
- Deleted an employee.
- Displayed the total number of employees.

### Validation and Error Handling

- Handled missing JSON files.
- Handled invalid JSON data.
- Prevented duplicate employee IDs.
- Validated salary values.
- Displayed meaningful error messages.
- Used the `json` module.
- Used `with open(...)` for file handling.

### Concepts Learned

- File handling
- JSON
- Reading and writing files
- CRUD operations
- Exception handling
- Data validation

---

### Task 3 - Comprehensions, Lambda, Map and Filter

Created `task_3_data_processing.py` using employee data.

The task included:

- Used list comprehension to get all employee names.
- Found employees earning more than 45,000.
- Found employees from the Development department.
- Created a dictionary containing employee names and salaries.
- Used `map()` to calculate yearly salaries.
- Used `filter()` to find employees earning more than 50,000.
- Used `lambda` with `sorted()` to sort employees by salary.
- Grouped employees by department.
- Calculated average salary for each department.
- Found the second-highest distinct salary.
- Kept the original employee list unchanged.
- Handled an empty employee list.

### Concepts Learned

- List comprehension
- Dictionary comprehension
- Lambda functions
- `map()`
- `filter()`
- `sorted()`
- Data grouping
- Average calculation
- Data processing

---

## Testing Requirements Covered

The following cases were tested:

- Missing employee JSON file
- Empty employee JSON file
- Duplicate employee ID
- Invalid salary
- Empty employee list

---

## Key Concepts Learned

During Day 2, I learned and practiced:

- *args
- **kwargs
- Functions
- Closures
- Decorators
- Type hints
- Docstrings
- File handling
- JSON
- CRUD operations
- Exception handling
- Input validation
- List comprehension
- Dictionary comprehension
- Lambda functions
- `map()`
- `filter()`
- `sorted()`
- Data grouping
- Data processing

---

## Learning Outcome

By completing the Day 2 tasks, I improved my understanding of advanced Python concepts and learned how to write more reusable and structured code.

I gained practical experience with decorators, closures, file handling, JSON data, comprehensions, lambda functions, map, filter, sorting, validation, and data processing.