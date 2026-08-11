#Task 9: Iterator and Generator
#Create:

#A custom iterator that returns numbers from 1 to 10.
#A generator function that returns even numbers from 1 to 50.

class My_iterator:
    def __init__(self,value):
        self.value = value
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.value:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration

iter = My_iterator(10)
print(iter.__next__())


## generator

def generator():
    for i in range(1,51):
            yield i
gen = generator()
print(next(gen))
