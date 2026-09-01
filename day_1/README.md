# Burnett Brucke Internship - Day 1

## Project Name
Python Programming Problems

## Description
This folder contains solutions for Python programming tasks (day_1 to day_3)

## Files Included
Task 1 – Calculator
User do numbers enter karta hai, phir operation choose karta hai (1-5 menu): Addition, Subtraction, Multiplication, Division, Modulus. Division aur Modulus mein zero-by-zero check hai taaki error na aaye (ZeroDivisionError avoid kiya gaya hai manually).

Task 2 – Dictionary Program (Student Marks Management)
Multiple students ka data ek dictionary mein store hota hai — har student ke 3 subjects ke marks, unka total, average, aur pass/fail status (average ≥ 40 pass). Sabka report print hota hai, aur end mein highest scorer dhoonda jata hai.

Task 3 – Exception Handling
Division perform karne ke liye:
ValueError – empty ya invalid input ke liye
ZeroDivisionError – zero se divide karne par
Custom exception NegativeNumberError – agar koi number negative ho
try/except/else/finally ka pura structure use kiya gaya hai.

Task 4 - Functions
build five function ->
is_prime() – number prime hai ya nahi
factorial() – factorial calculate karta hai
check_even_or_odd() – even/odd check karta hai
largest_number_from_list() – list ka largest number dhoondta hai
largest_number_from_list() – list ka average nikalta hai

Task 5 – Generator and Iterator Function

-> yield keyword use karke ek generator function banaya hai jo 1 se 50 tak ke even numbers ek-ek karke deta hai (memory-efficient way, list bina banaye).

-> NumberIterator class banayi hai jisme __iter__ aur __next__ methods implement hain, jisse ye object directly for loop mein use ho sake (1 se 10 tak numbers dega).

-> sys.getsizeof() se compare kiya gaya hai ki 10 lakh numbers wali list kitni memory leti hai vs same numbers wala generator. Result: List ~8.4 MB ki hai jabki generator sirf 200 bytes ka — yani list generator se ~42,244 guna zyada memory leti hai. Ye result memory_results.txt mein save bhi hota hai.


Task 6 – List Operations
Ek list of numbers par operations kiye gaye hain
Sare Operations bina built-in function use kare perform huye he  
largest number in a list
smallest number in a list
remove duplicate numbers from a list without using 
Sum of all numbers from a list
Second largest distinct number nikalna
Saath hi same operations from scratch (bina built-in functions ke, loops use karke) bhi dikhaye gaye hain — ye samajhne ke liye ki andar se kaise kaam karta hai.

Task 7 – OOP (Inheritance & Method Overriding)
Person base class hai (name, email, age). 2 child classes hain: Student (course, marks) aur Teacher (subject, salary). Dono ne display_dashboard() method ko override kiya hai apna alag dashboard dikhane ke liye — ye polymorphism ka example hai.

Task 8 – String Operations
All string operation is performed without using built-in functions
total characters count
total words count
words ko reverse order mein join karke sentence reverse
dictionary use karke har word ki frequency count
Ek alag word lekar palindrome check

Task 9 – Basic Python Program
User se Name, Age, Email, City input liya jata hai aur phir sabko formatted tarike se print kiya jata hai. Ye basic input() aur print() ka use sikhata hai.

## Tech Stack
- Python 3

## How to Run
Run any task individually:
```bash
python calculator.py
python dictionary_operations.py
python exception_handling.py
python functions.py
python generator_and_iterator.py
python list_operations.py
python oops.py
python string_operations.py
python user_information.py
```
