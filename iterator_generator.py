import sys
# Custom Iterator 
class NumberIterator:
    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= 10:
            value = self.number
            self.number += 1
            return value
        else:
            raise StopIteration


# Generator
def even_numbers():
    for i in range(2, 51, 2):
        yield i


# Memory Comparison 
numbers_list = list(range(1000000))
numbers_generator = (i for i in range(1000000))

print("Memory used by List:", sys.getsizeof(numbers_list), "bytes")
print("Memory used by Generator:", sys.getsizeof(numbers_generator), "bytes")


# Iterator Output
print("\nNumbers from Custom Iterator:")
for num in NumberIterator():
    print(num, end=" ")


# Generator Output 
print("\n\nEven Numbers from Generator:")
for num in even_numbers():
    print(num, end=" ")