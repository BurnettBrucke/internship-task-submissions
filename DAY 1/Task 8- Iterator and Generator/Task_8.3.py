# Compare the memory size of:

# A list containing one million numbers
# A generator containing one million numbers
# Write your observation in the README file.

import sys

my_list = [i for i in range(1000000)]
my_generator = (i for i in range(1000000))

print(f"List size: {sys.getsizeof(my_list)} bytes")
print(f"Generator size: {sys.getsizeof(my_generator)} bytes")