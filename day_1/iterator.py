# Task 9: Iterator and Generator
# Create:
#  A custom iterator that returns numbers from 1 to 10.
class OneToTenNumbers:
    def __init__(self):
        # Start at 1
        self.current = 1

    def __iter__(self):
        # Returns the iterator object itself
        print(self)
        return self

    def __next__(self):
        # Check if the limit is exceeded
        if self.current > 10:
            raise StopIteration
        
        # Save the current value, increment, and return
        val = self.current
        self.current = self.current + 1
        return val

iterator = OneToTenNumbers()
for num in iterator:
    print(num)


#  A generator function that returns even numbers from 1 to 50.
def generator_function_for_even():
    for i in range(1, 51):
        if i % 2 == 0:
            yield i

for even in generator_function_for_even():
    print(even, end=" ")


#  A list containing one million numbers
my_list = [i for i in range(1, 100000)]
# print(my_list)

import sys
memory = sys.getsizeof(my_list)
print(memory)       # It contains 800984 bytes space in the memory


#  A generator containing one million numbers
def one_million_numbers_generator():
    for i in range(1, 100000):
        yield i

for number in one_million_numbers_generator():
    # print(number)
    pass

# import sys
memory = sys.getsizeof(one_million_numbers_generator)
print(memory)       # It contains only 160 bytes space in the memory


# Compare the memory size of:
''' List contains all 1 million data in memory, therefore it is not memory efficient.'''

''' Generator contains only 160 bytes space in the memory, if the numbers 
    will 10 crore, it contains same 160 bytes space in the memory
    because it takes one value at a time, It is not contain whole 
    10 crore data in memory, therefore it is memory efficient. '''

# Write your observation in the README file.