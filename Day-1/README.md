# Python Internship - Day 1

This repository contains the Python tasks completed during **Day 1 of my Python Internship**.

The purpose of these tasks is to build a strong foundation in Python by practicing basic syntax, conditions, loops, strings, collections, functions, file handling, JSON, and error handling.

---

## 📁 Project Structure

```text
Day-1/
│
├── database/
│   └── student_data.json
│
├── task_1_basics.py
├── task_2_conditions_loops.py
├── task_3_string.py
├── task_4_collection.py
├── task_5_student_manager.py
└── README.md
```

---

# 📚 Tasks

## Task 1 - Python Basics

The first task focuses on understanding the fundamentals of Python programming.

### Topics Covered

- Variables
- Data types
- Input and output
- Type conversion
- Arithmetic operators
- Comparison operators
- Basic calculations
- Basic Python syntax

### File

```text
task_1_basics.py
```

---

## Task 2 - Conditions & Loops

The second task focuses on controlling program flow using conditions and loops.

### Topics Covered

- `if`
- `elif`
- `else`
- `for` loops
- `while` loops
- `break`
- `continue`
- Conditional logic
- Input validation
- Basic problem solving

### File

```text
task_2_conditions_loops.py
```

---

## Task 3 - Strings

The third task focuses on working with strings and common string operations.

### Topics Covered

- String creation
- String indexing
- String slicing
- String methods
- Searching within strings
- String manipulation
- String formatting
- `f-strings`

### File

```text
task_3_string.py
```

---

## Task 4 - Collections

The fourth task focuses on Python's built-in collection data types.

### Topics Covered

- Lists
- Tuples
- Sets
- Dictionaries
- Adding elements
- Removing elements
- Updating elements
- Iterating through collections
- Dictionary methods
- Working with nested dictionaries

### File

```text
task_4_collection.py
```

---

# 🎓 Task 5 - Student Marks Manager

The fifth task is a practical project that combines the Python concepts learned in the previous tasks.

It is a **menu-driven student marks management system**.

The application stores student names along with their marks in different subjects.

---

## ✨ Features

The Student Marks Manager provides the following features:

### 1. View All Students

Displays all students along with their subject marks.

### 2. Search Student

Allows the user to search for a student by name.

### 3. Update Marks

Allows the user to update the marks of an existing student.

### 4. Add New Student

Allows the user to add a new student and enter their marks.

### 5. Student Result

Calculates:

- Total marks
- Average marks
- Pass/Fail result

### 6. Student Rank

Calculates the total marks of students and allows the user to find a particular rank.

For example:

```text
Rank 1
Rank 2
Rank 3
```

### 7. Save Data to JSON

Saves the current student data into a JSON file.

### 8. Load Data from JSON

Loads student data from a JSON file into the program.

### 0. Exit

Exits the application.

---

# 🗃️ Database

The student data is stored using a JSON file.

```text
database/
└── student_data.json
```

JSON is used as a simple form of persistent storage for this project.

Instead of hardcoding the student data directly inside the Python program, the program can load the data from the JSON file.

---

## 📄 Example JSON Data

```json
{
    "Mayank": {
        "math": 85,
        "python": 90,
        "english": 78
    },
    "Rahul": {
        "math": 70,
        "python": 88,
        "english": 65
    },
    "Aman": {
        "math": 100,
        "python": 95,
        "english": 98
    },
    "Priya": {
        "math": 40,
        "python": 40,
        "english": 40
    },
    "Neha": {
        "math": 35,
        "python": 90,
        "english": 85
    }
}
```

---

# 🧠 Concepts Used in Task 5

The Student Marks Manager combines multiple Python concepts.

### Python Concepts

- Variables
- Functions
- Dictionaries
- Nested dictionaries
- Loops
- Conditional statements
- `match-case`
- User input
- String methods
- List/dictionary operations
- Sorting

### Built-in Functions

- `sum()`
- `len()`
- `sorted()`
- `all()`

### File Handling

- `open()`
- Reading files
- Writing files
- JSON file handling

### JSON

- `json.load()`
- `json.dump()`

### Error Handling

- `try`
- `except`
- `FileNotFoundError`
- `JSONDecodeError`
- Input validation

---

# 🔄 Program Flow

The general flow of the application is:

```text
Start
  │
  ▼
Load Student Data
  │
  ▼
Display Main Menu
  │
  ├── 1 → View Students
  │
  ├── 2 → Search Student
  │
  ├── 3 → Update Marks
  │
  ├── 4 → Add Student
  │
  ├── 5 → Check Result
  │
  ├── 6 → Find Rank
  │
  ├── 7 → Save JSON
  │
  ├── 8 → Load JSON
  │
  └── 0 → Exit
```

After completing an operation, the program returns to the main menu.

---

# 💾 JSON Data Flow

The application uses JSON for persistent storage.

### Loading

```text
JSON File
    ↓
json.load()
    ↓
Python Dictionary
    ↓
Student Manager
```

### Saving

```text
Student Manager
    ↓
Python Dictionary
    ↓
json.dump()
    ↓
JSON File
```

This allows student data to remain available even after the program is closed.

---

# ▶️ How to Run

Make sure Python is installed on your system.

Navigate to the `Day-1` directory:

```bash
cd Day-1
```

Then run:

```bash
python task_5_student_manager.py
```

---

# 🛠️ Requirements

The project uses Python's standard library.

No external packages are required.

The main modules used are:

```python
import json
```

---

# 📌 Day 1 Summary

| Task | Topic | File |
|------|-------|------|
| Task 1 | Python Basics | `task_1_basics.py` |
| Task 2 | Conditions & Loops | `task_2_conditions_loops.py` |
| Task 3 | Strings | `task_3_string.py` |
| Task 4 | Collections | `task_4_collection.py` |
| Task 5 | Student Marks Manager | `task_5_student_manager.py` |

---

## 👨‍💻 Project

**Python Internship - Day 1**

The project demonstrates the practical application of Python fundamentals through a student marks management system with JSON-based data storage.