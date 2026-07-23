def add():
    a=float(input("Enter the first Number:"))
    b=float(input("Enter the Second Number:"))
    print(a+b)

def sub():
    a=float(input("Enter the first Number:"))
    b=float(input("Enter the Second Number:"))
    print(a-b)

def mul():
    a=float(input("Enter the first Number:"))
    b=float(input("Enter the Second Number:"))
    print(a*b)

def div():
    a=float(input("Enter the first Number:"))
    b=float(input("Enter the Second Number:"))
    try:
        print(a/b)
    except ZeroDivisionError:
        print("Cannot be divided by Zero")

def mod():
    a=float(input("Enter the first Number:"))
    b=float(input("Enter the Second Number:"))
    print(a%b)        

while True:
    choice=int(input(f"""
    1.Addition
    2.Subtraction
    3.Multiplication
    4.Divison
    5.Modulus
    6.Exit
    
    Enter the Opertion you want to perform:
    """))
    match choice:
        case 1:
            print("Performing Addition")
            add()
        case 2:
            print("Performing Subtraction")
            sub()
        case 3:
            print("Performing Multiplication")
            mul()
        case 4:
            print("Performing Division")
            div()
        case 5:
            print("Performing Modulus")
            mod()
        case 6:
            break
        case _:
            print("Invlid Input")