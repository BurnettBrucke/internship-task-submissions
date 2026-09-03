# Calculate rectangle area and perimeter.
def area_of_rectangle(l,b):
    return l*b

def perimeter_of_rectangle(l,b):
    return 2*(l+b)

len = float(input("Enter length : "))
bre = float(input("Enter breadth : "))

print("Area of Rectangle is : ", area_of_rectangle(len,bre))
print("Perimeter of Rectangle is : ", perimeter_of_rectangle(len,bre))
