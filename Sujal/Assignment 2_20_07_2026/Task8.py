class NegativeNumber(Exception):
    pass
def divison(a,b):
    if a<0 or b<0:
        raise NegativeNumber("Negative Numbers are not allowed")
    return a/b

try:
    a=(input("Enter the first number:"))
    b=(input("Enter the Second number:"))
    
    if a.strip()==""or b.strip()=="":
        raise ValueError("Input Cannot be Empty")
    
    c=int(a)
    d=int(b)
    
    print(divison(c,d))

except ZeroDivisionError:
    print("Number cannot be divided by zero")
except ValueError:
    print("Number can only be int")
except NegativeNumber as e:
    print(e)    