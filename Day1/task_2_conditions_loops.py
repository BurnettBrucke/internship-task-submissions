def input_number():
    return input("Enter the number: ")


def checking_pos_neg():
    number = float(input("Enter the number: "))
    if number > 0:
        print(f"{number} is a positive number")
    elif number < 0:
        print(f"{number} is a negative number")
    else:
        print(f"{number} is a zero")


# checking_pos_neg()


def check_even_odd():
    num = int(input("Enter the number: "))
    if num % 2 == 0:
        print(f"{num} is a Even Number")
    else:
        print(f"{num} is a odd number")


# check_even_odd()


def largest_of_three():
    a = int(input_number())
    b = int(input_number())
    c = int(input_number())

    if a >= b and a >= c:
        print(f"{a} is greater")
    elif b >= a and b >= c:
        print(f"{b} is greater")
    else:
        print(f"{c} is greater")


# largest_of_three()


def multiplication_table():
    n = int(
        input(
            "Enter the number for which you want to generate the multiplication table: "
        )
    )
    i = 1
    while i <= 10:
        print(f"{n} x {i} = {n*i}")
        i = i + 1


# multiplication_table()


def sum_from_1to_n():
    sum = 0
    n = int(input_number())
    for i in range(n + 1):
        sum = sum + i

    print(sum)


# sum_from_1to_n()


def check_number_is_prime():
    n = int(input_number())
    count = 0
    for i in range(1, n + 1):
        if n % i == 0:
            count = count + 1
    if count > 2:
        print(f"Number {n} is not a prime number")
    else:
        print(f"{n} is a Prime Number")


# check_number_is_prime()


def even_number_from_1to100():
    for i in range(1, 101):
        if i % 2 == 0:
            print(i)


# even_number_from_1to100()
