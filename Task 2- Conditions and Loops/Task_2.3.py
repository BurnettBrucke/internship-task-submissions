# Find the largest of three numbers.
def largest_number(a,b,c):
    if a>b and a>c:
        print(f"{a} is bigger than {b} and {c}")
    elif b>a and b>c:
        print(f"{b} is bigger than {a} and {c}")
    else:
        print(f"{c} is bigger than {a} and {b}")

num1 = int(input("Enter number 1 : "))
num2 = int(input("Enter number 2 : "))
num3 = int(input("Enter number 3 : "))

largest_number(num1, num2, num3)