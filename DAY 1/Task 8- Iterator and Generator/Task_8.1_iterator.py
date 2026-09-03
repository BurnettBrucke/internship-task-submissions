# Create a custom iterator that returns numbers from 1 to 10.

class MyNumber:
    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= 10:
            val = self.number
            self.number += 1
            return val
        else:
            raise StopIteration

numbers = MyNumber()
for num in numbers:
    print(num)