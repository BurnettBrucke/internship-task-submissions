# Burnett Brucke Internship - Task 2

## Project Name
Python Programming Tasks-2

## Description
This folder contains solutions for Python programming tasks (Task 1 to Task 9).

## Files Included
- Task 1 – Basic Python Program
User se Name, Age, Email, City input liya jata hai aur phir sabko formatted tarike se print kiya jata hai. Ye basic input() aur print() ka use sikhata hai.

Task 2 – Calculator
User do numbers enter karta hai, phir operation choose karta hai (1-5 menu): Addition, Subtraction, Multiplication, Division, Modulus. Division aur Modulus mein zero-by-zero check hai taaki error na aaye (ZeroDivisionError avoid kiya gaya hai manually).

Task 3 – List Operations
Ek list of numbers par operations kiye gaye hain:

max()/min() se largest/smallest
set() se duplicates remove
sum() se total
Second largest distinct number nikalna
Saath hi same operations from scratch (bina built-in functions ke, loops use karke) bhi dikhaye gaye hain — ye samajhne ke liye ki andar se kaise kaam karta hai.

Task 4 – String Operations
Sentence input lekar:

len() se total characters count
split() se total words count
Words ko reverse order mein join karke sentence reverse
Dictionary use karke har word ki frequency count
Ek alag word lekar palindrome check (str1 == str1[::-1])

Task 5 – Dictionary Program (Student Marks Management)
Multiple students ka data ek dictionary mein store hota hai — har student ke 3 subjects ke marks, unka total, average, aur pass/fail status (average ≥ 40 pass). Sabka report print hota hai, aur end mein highest scorer dhoonda jata hai.

Task 6 – Functions
5 alag functions banaye gaye hain, har ek type hints aur docstring ke saath:

check_prime() – number prime hai ya nahi
cal_fact() – factorial calculate karta hai
check_even_odd() – even/odd check karta hai
find_largest() – list ka largest number dhoondta hai
avg() – list ka average nikalta hai

Task 7 – OOP (Inheritance & Method Overriding)
Person base class hai (name, email, age). Do child classes hain: Student (course, marks) aur Teacher (subject, salary). Dono ne display_dashboard() method ko override kiya hai apna alag dashboard dikhane ke liye — ye polymorphism ka example hai.

Task 8 – Exception Handling
Division perform karne ke liye:

ValueError – empty ya invalid input ke liye
ZeroDivisionError – zero se divide karne par
Custom exception NegativeNumberError – agar koi number negative ho
try/except/else/finally ka pura structure use kiya gaya hai.

Task 9_1 – Custom Iterator
NumberIterator class banayi hai jisme __iter__ aur __next__ methods implement hain, jisse ye object directly for loop mein use ho sake (1 se 10 tak numbers dega).

Task 9_2 – Generator Function
yield keyword use karke ek generator function banaya hai jo 1 se 50 tak ke even numbers ek-ek karke deta hai (memory-efficient way, list bina banaye).

Task 9_3 – Memory Comparison (List vs Generator)
sys.getsizeof() se compare kiya gaya hai ki 10 lakh numbers wali list kitni memory leti hai vs same numbers wala generator. Result: List ~8.4 MB ki hai jabki generator sirf 200 bytes ka — yani list generator se ~42,244 guna zyada memory leti hai. Ye result memory_results.txt mein save bhi hota hai.

## Tech Stack
- Python 3

## How to Run
Run any task individually:
```bash
python task1.py
python task2.py
python task3.py
python task4.py
python task5.py
python task6.py
python task7.py
python task8.py
python task9_1.py
python task9_2.py
python task9_3.py
```

