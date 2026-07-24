def is_prime(num: int) -> bool:
   
    if num <= 1:
        return False

    for i in range(2, num):
        if num % i == 0:
            return False

    return True


def factorial(num: int) -> int:
    
    fact = 1

    for i in range(1, num + 1):
        fact = fact * i

    return fact


def even_or_odd(num: int) -> str:
    
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"


def largest_number(numbers: list[int]) -> int:
   
    largest = numbers[0]

    for num in numbers:
        if num > largest:
            largest = num

    return largest


def average(numbers: list[int]) -> float:
   
    total = 0

    for num in numbers:
        total = total + num

    return total / len(numbers)


# ---------------- Main Program ----------------

number = int(input("Enter a number: "))

print("Prime:", is_prime(number))
print("Factorial:", factorial(number))
print("Even/Odd:", even_or_odd(number))

nums = list(map(int, input("Enter numbers separated by space: ").split()))

print("Largest Number:", largest_number(nums))
print("Average:", average(nums))