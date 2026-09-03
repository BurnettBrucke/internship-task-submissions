
# End-of-Day (EOD) Report - Day 1

**Intern Name:** Ruchita prajapat 
**Date:** September 1, 2026  
**Training Module:** Python Basics, Control Flow, Strings, Collections, and Functions  
**Repository Branch:** `burnettbrucke-intern-task-ruchita`  

---

## 1. Completed Work

### Task 1: Python Basics & Input Handling
* Created scripts `task_1.1.py` through `task_1.5.py` to handle formatted user intros, arithmetic operations, unit conversions, geometry formulas, and salary calculations.
* Implemented strict input validation to prevent invalid data types and handled division by zero exceptions.

### Task 2: Conditions and Loops
* Created scripts `task_2.1.py` through `task_2.7.py` demonstrating conditional branching (`if-elif-else`) and iteration controls (`for` and `while` loops).
* Implemented modular functions for mathematical checks (Prime numbers, Multiplication tables, Sum of series, Even/Odd detection).

### Task 3: String Operations
* Solved string manipulation problems including reversing sentences, checking palindromes, counting vowels/consonants/words, stripping extra spaces, character frequency mapping, and finding non-repeating characters without using external libraries.

### Task 4: Lists & Dictionaries
* Solved array manipulation problems including min/max extraction, second-largest element discovery without complete sorting, duplicate removal while preserving order, and dictionary aggregation for high/low/average marks calculation.

### Task 5: Student Marks Manager (Mini Project)
* Developed an interactive menu-driven CLI application (`task_5.py`).
* Implemented CRUD features: Add student, Update marks, Delete student, View records, Search by name, Pass/Fail decision (minimum 40 mark criteria per subject), and Top scorer calculation.
* Implemented **Bonus Feature**: Dynamic saving and loading of student data using `students.json`.

---

## 2. Key Learnings

1. **Input Handling & Defensiveness:** Learned the importance of wrapping raw user input inside `try-except` blocks to handle non-numeric entries gracefully.
2. **Algorithm Efficiency:** Implemented logic to find the second-largest distinct element in a single traversal without using full `.sort()`.
3. **Control Flow Mastery:** Gained clarity on using `break`, `continue`, and return statements inside loops.
4. **Data Persistence:** Learned how to serialize Python dictionaries into JSON format and deserialize them back upon script launch.

---

## 3. Blockers Encountered & Resolutions

* **Blocker 1:** Handling `ZeroDivisionError` in the calculator module during runtime.  
  * *Resolution:* Added a check `if denominator == 0:` before executing division or modulus operations.
* **Blocker 2:** Duplicate student entry in Task 5 causing data overwrite.  
  * *Resolution:* Added explicit validation to check if the student name already exists in the primary dictionary before creating a new entry.

---

## 4. Pending Work

* **None.** All Day 1 workbook requirements, edge test cases, README documentation, and EOD reporting have been completed and verified.