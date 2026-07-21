class NumberIterator:
    """Iterator that yields numbers from 1 to 10 (inclusive)."""
 
    def __init__(self, start=1, end=10):
        self.current = start   # tracks where we currently are
        self.end = end         # the last number to return
 
    def __iter__(self):
        # An iterator must return itself from __iter__
        return self
 
    def __next__(self):
        # This runs every time next() is called on the object
        if self.current > self.end:
            # No more numbers left -> tell Python to stop looping
            raise StopIteration
        value = self.current
        self.current += 1      # move to the next number for next time
        return value
 
 

print("Custom Iterator Output (1 to 10):")
numbers = NumberIterator(1, 10)
 
    # Because NumberIterator implements __iter__ and __next__,
    # we can use it directly in a for loop, just like a list.
for num in numbers:
    print(num, end=" ")
    print("\n")
 