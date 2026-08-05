
def validate_salaries(salaries: tuple[float, ...]) -> None:
    if not salaries:
        raise ValueError("At least one salary must be provided.")

    for salary in salaries:
        if not isinstance(salary, (int, float)):
            raise ValueError(f"Invalid salary: {salary}")

        if salary < 0:
            raise ValueError("Salary cannot be negative.")


# 1. Create a function that accept employee details using ** kwargs
def employee_details(**kwargs):

    # Accessing specific keys safely using .get()
    name = kwargs.get("name")
    print(f"Name : {name}")

    # Iterating through all passed keyword arguments
    for key, values in kwargs.items():
            print(f"{key} : {values}")

# Calling the function with varying named parameters
employee_details(name='rahul', age=25, city='Shajapur')
# -----------------------------------------------------------------------------------------------------------

# 2. Create a function that accepts any number of salaries using *args and returns 
# total, average, highest and lowest salary.
def any_number_of_salaries(*args):
    if args:
        count = 0
        total = 0
        highest = args[0]
        lowest = args[0] 
        for i in args:
            total = total + i
            count = count +1 
            average = total/count
            # First of all we will assign args[0] to highest value then 
            # we will check which one is highest, if we found one, then 
            # we will assign those value to highest.
            if i > highest :
                highest = i
            if i < lowest :
                lowest = i
        print("Lowest Value is : ", lowest)    
        print("Highest Value is : ", highest)
        print("Total Salary is : ", total)  
        print("Average is : ", average)

    elif args != float(args) :
        print("Invalid Salary Values !")
    else:
        print("Please Input some salary !")


any_number_of_salaries(2345.45, 24354, 'rahul')


# 3. Create a closure that maintains a running total.



# 4. Create a decorator named execution_logger that displays the function name,
#    start message, completion message and execution time.

def execution_logger():
    pass


execution_logger()

# 5. Apply the decorator to at least three functions.
