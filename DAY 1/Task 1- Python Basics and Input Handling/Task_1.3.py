# Convert Celsius to Fahrenheit.

def celcius_to_fahrenheit(cel):
    fah = (9/5)*cel+32
    return fah

def fahrenheit_to_celcius(fah):
    cel = (5/9)*(fah-32)
    return cel

print("Celcius to Fahrenheit : ",celcius_to_fahrenheit(int(input("Enter celcius : "))))
print("Fahrenheit to Celcius : ",fahrenheit_to_celcius(int(input("Enter fahrenheit : "))))