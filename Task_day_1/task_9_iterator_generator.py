# Task 9: Iterator and Generator
# 1. Custom Iterator: Returns numbers from 1 to 10
class NumberIterator:
    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= 10:
            current_number = self.number
            self.number += 1
            return current_number
        raise StopIteration

print("Custom Iterator (1 to 10):")

numbers = NumberIterator()

for number in numbers:
    print(number, end=" ")

# 2. Generator: Returns even numbers from 1 to 50
def even_number_generator():
    for number in range(1, 51):
        if number % 2 == 0:
            yield number

print("\n\nEven Numbers from 1 to 50:")

for number in even_number_generator():
    print(number, end=" ")

# 3. Memory Comparison
import sys

one_million_list = list(range(1_000_000))
one_million_generator = (number for number in range(1_000_000))

list_memory = sys.getsizeof(one_million_list)
generator_memory = sys.getsizeof(one_million_generator)

print("\n\nMemory Comparison:")
print(f"List memory: {list_memory} bytes")
print(f"Generator memory: {generator_memory} bytes")