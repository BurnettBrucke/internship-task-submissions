def check_number():
    try:
        number = float(input("Enter a number : "))
        if number > 0:
            print("The number is positive.")
        elif number < 0 :
            print("The number is negative.")
        else:
            print("The number is zero.")
    except ValueError:
        print("please enter an vaild number.")

def check_even_odd():
    try:
        number = int(input("Enter a number : "))
        if number %2 == 0:
            print(f"{number} is even number.")
        else:
            print(f"{number} is odd number.")
    except ValueError:
        print("Please enter an valid number.")

def find_the_largest_number():
    a = int(input("Enter first number : "))
    b = int(input("Enter second number : "))
    c = int(input("Enter third number : "))
    if a>= b and a >= c:
        largest_num = a
    elif b >= c and b >= a:
        largest_num = b
    else:
        largest_num = c
    print(f"Largest number is {largest_num}.")

def multiplication_table():
    try :
        number = int(input("Enter the number : "))
        if number < 0:
            print("you have enterd negative number.")
        for i in range(1,11):
            print(f"{i} x {number} = {i*number}")
    except ValueError:
        print("please enter an vaild number")

def sum_of_number():
    try:
        number = int(input("Enter the number : "))
        total = 0
        if number < 0:
            print("please enter a vaild number")
            return
        for n in range(1,number+1):
            total += n
        print(f"The sum is : {total}")
    except ValueError:
        print("please enter an vaild number")

def check_prime():
    number = int(input("Enter an number : "))
    try:
        if number <= 1:
            return "Not prime"
        if number == 2:
            return "Prime"
        for i in range(3,int(number**0.5)+1):
            if number % i == 0:
                return "Not prime"
        return "Prime"
    except ValueError:
        print("please enter an vaild number")
    

def even_number_using_for():
    for i in range(1,101):
        if i % 2 == 0:
            print(i, end=",")    
def even_number_using_while():
    i = 1
    while i <=100:
        if i % 2 == 0:
            print(i, end=",")
        i += 1

def main():
    print("===== Task 2: Conditions and Loops =====")

    print("\n--- Positive, Negative or Zero ---")
    check_number()

    print("\n--- Even or Odd ---")
    check_even_odd()

    print("\n--- Largest of Three Numbers ---")
    find_the_largest_number()

    print("\n--- Multiplication Table ---")
    multiplication_table()


    print("\n--- Sum from 1 to N ---")
    sum_of_number()

    print("\n--- Prime Number ---")
    result = check_prime()
    print(result)

    print("\n--- Even Numbers from 1 to 100 ---")
    even_number_using_for()
    print()

    print("\n--- Even Numbers using While Loop ---")
    even_number_using_while()

if __name__ == "__main__":
    main()