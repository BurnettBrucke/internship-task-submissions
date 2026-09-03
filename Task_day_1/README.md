# Python and Django Training - Day 1 Submission

This repository contains the Day 1 task submissions for the Python and Django Internship Program. All programs are modularized into specific task folders based on their functional topics.

---

##  Repository Structure

```text
Task_day_1/
├── task_1_basics/
│   ├── task_1.1.py    # User Information Formatting
│   ├── task_1.2.py    # Basic Calculator (+, -, *, /, %)
│   ├── task_1.3.py    # Celsius to Fahrenheit Converter
│   ├── task_1.4.py    # Rectangle Area & Perimeter
│   └── task_1.5.py    # Salary Increment Calculator
│
├── task_2_Conditions_Loops/
│   ├── task_2.1.py    # Positive, Negative, or Zero Check
│   ├── task_2.2.py    # Even or Odd Check
│   ├── task_2.3.py    # Largest of Three Numbers
│   ├── task_2.4.py    # Multiplication Table Generator
│   ├── task_2.5.py    # Sum of 1 to N
│   ├── task_2.6.py    # Prime Number Checker
│   └── task_2.7.py    # Even Numbers 1 to 100
│
├── task_3_strings/     # String operations & manipulation tasks
├── task_4_collections/ # Lists and Dictionaries tasks
│
├── task_5_student_manager/
│   ├── students.json   # JSON storage for student records (Bonus)
│   └── task_5.py       # Menu-driven Student Marks Manager CLI
│
├── README.md           # Setup and Execution Instructions
└── eod_report.md       # End-of-Day Progress Report

Here are some extra task that is task 7 for object oriented programming.

// run task :python task_7_opps.py

//for task 9 : python task_9_iterator_generator.py

Task 9: Iterator and Generator

 Observation

A list stores all one million numbers in memory at the same time, so it requires significantly more memory.

A generator does not store all the numbers at once. It generates each value only when required, so it uses very little memory.

For example, a list containing one million numbers may require several megabytes of memory, while the generator object itself requires only a few hundred bytes.

Therefore, generators are much more memory-efficient than lists when working with large amounts of data.

### Conclusion

- Lists store all values in memory.
- Generators produce values one at a time.
- Generators are more memory-efficient for large datasets.
- Generators are useful when all values do not need to be stored simultaneously.