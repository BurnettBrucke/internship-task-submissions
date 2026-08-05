# A generator function that returns even numbers from 1 to 50.

def generator_function_for_even():
    for i in range(1, 51):
        if i % 2 == 0:
            yield i

# # Consume the generator using a loop
for even in generator_function_for_even():
    print(even, end=" ")