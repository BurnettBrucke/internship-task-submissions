class NumberIterater:
    def __init__(self):
        self.number = 1
    def __iter__(self):
        return self

    def __next__(self):
        if self.number > 10:
            raise StopIteration
        
        current = self.number
        self.number += 1

        return current

value = NumberIterater()
for number in value:
    print(number)


def even_number():
    for number in range(1,51):
        if number % 2 == 0:
            yield number

even_numbers = even_number()
for num in even_numbers:
    print(num)



import sys

numbers_list = list(range(1_000_000))
numbers_generator = (number for number in range(1_000_000))

print("List memory:", sys.getsizeof(numbers_list), "bytes")
print("Generator memory:", sys.getsizeof(numbers_generator), "bytes")