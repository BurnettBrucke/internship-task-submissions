def find_largest_smallest():
    list1 = [int(x) for x in input("Enter element separated by space: ").split()]
    largest = float("-inf")
    smallest = float("inf")
    for i in range(len(list1)):
        if list1[i] > largest:
            largest = list1[i]
        else:
            continue
        if list1[i] < smallest:
            smallest = list1[i]
    print(
        f"Largest of the list is : {largest} and smallest of the list is : {smallest}"
    )


# find_largest_smallest()


def find_second_largest():
    list1 = [int(x) for x in input("Enter element separated by space: ").split()]
    largest = float("-inf")
    second_largest = float("-inf")
    if len(list1) < 2:
        return print(-1)
    for i in range(len(list1)):
        if list1[i] > largest:
            second_largest = largest
            largest = list1[i]

        elif list1[i] > second_largest and list1[i] != largest:
            second_largest = list1[i]

    print(second_largest)


# find_second_largest()


def remove_duplicate():
    list2 = [int(x) for x in input("Enter the element separated by space: ").split()]
    seen = set()
    result = []
    for num in list2:
        if num not in seen:
            seen.add(num)
            result.append(num)
    print(result)


# remove_duplicate()


def separate_even_odd():
    list1 = [int(x) for x in input("Enter the elements separated by space: ").split()]
    even = []
    odd = []
    for num in list1:
        if num % 2 == 0:
            even.append(num)
        else:
            odd.append(num)
    print(f"The even list is {even} and the odd list is {odd}")


# separate_even_odd()


def count_frequency_of_each_number():
    list1 = [int(x) for x in input("Enter the number separated by space: ").split()]
    frequency = {}
    for num in list1:
        frequency[num] = frequency.get(num, 0) + 1
    print(frequency)


# count_frequency_of_each_number()


def marks_high_low_average():
    marks = {"ankur": 85, "aditya": 90, "ajay": 89, "dev": 95}

    first_student = next(iter(marks))
    highest_scorer = first_student
    lowest_scorer = first_student

    total_marks = 0
    student_count = 0

    for student in marks:
        score = marks[student]

        total_marks += score
        student_count += 1

        if score > marks[highest_scorer]:
            highest_scorer = student
        if score < marks[lowest_scorer]:
            lowest_scorer = student

    averge_of_marks = total_marks / student_count

    print(
        f"Highest Scorer: {highest_scorer} marks of highest scorer {marks[highest_scorer]}"
    )
    print(
        f"lowest Scorer : {lowest_scorer} marks of lowest scorer {marks[lowest_scorer]}"
    )
    print(f"Average marks: {averge_of_marks}")


marks_high_low_average()
