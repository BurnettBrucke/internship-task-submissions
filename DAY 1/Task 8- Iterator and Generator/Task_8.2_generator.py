# Create a generator function that returns even numbers from 1 to 50.
def numbers():
    for i in range(1,51):
        if i%2 == 0:
            yield i

for num in numbers():
    print(num)
