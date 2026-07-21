def operations(numbers):
    print(f"Original List: {numbers}")

    # Largest Element
    print(f"Largest Number: {max(numbers)}")

    # Smallest Element
    print(f"Smallest Number: {min(numbers)}")

    #Removing Duplicates
    unique = []
    for num in numbers:
        if num not in unique:
            unique.append(num)

    print(f"List after Removing Duplicates: {unique}")

    # sum of all
    total = 0
    for num in numbers:
        total += num

    print(f"Sum of all Elements: {total}")

   #SEcond Largest
    largest = second_largest = float('-inf')

    for num in numbers:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num

    if second_largest == float('-inf'):
        print("Second Largest Distinct Number does not exist.")
    else:
        print(f"Second Largest Distinct Number: {second_largest}")


numbers = list(map(int, input("Enter the elements of the list: ").split()))
operations(numbers)