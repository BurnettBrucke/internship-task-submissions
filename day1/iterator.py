'''
Task 9: Iterator and Generator
Create:

A custom iterator that returns numbers from 1 to 10.
A generator function that returns even numbers from 1 to 50.
Compare the memory size of:

A list containing one million numbers
A generator containing one million numbers
Write your observation in the README file.'''

# l=[1,2,3,4,5,6,7,8,9,10]
# it=iter(l)
# print(next(it))

#  custom iterator class se bnata hai 
class number:
    def __init__(self):
        self.num=1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.num<=10:
            value=self.num
            self.num+=1
            return value
        else:
            raise StopIteration
object=number()
for i in object:
    print(i)

# generator
# function se bnata hai 
print("\ngenerator ")
def num():
    for i in range(1,51):
        if i%2==0:
            yield i

for i in num():
    print(i)