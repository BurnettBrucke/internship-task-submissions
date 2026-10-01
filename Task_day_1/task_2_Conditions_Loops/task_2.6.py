#  Check whether a number is prime.

def is_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                print(num, "is not a prime number")
                break
    else:
        print(num, "is a prime number")

num  = int(input("Enter a number:"))
is_prime(num)