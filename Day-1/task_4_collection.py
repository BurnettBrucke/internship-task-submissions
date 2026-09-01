def largest_smallest_element(nums:list):
    try:
        largest_elemnt = nums[0]
        smallest_elemnt = nums[0]
        for n in nums:
            if n > largest_elemnt:
                largest_elemnt = n
            if n < smallest_elemnt:
                smallest_elemnt = n
        print(f"Largest number in the list is {largest_elemnt} and the smallest number is {smallest_elemnt}.")
    except IndexError:
        print("Please enter an vaild list with more then two elemnet")

def find_second_largest(nums: list):
    if not nums:
        print("Please enter a non-empty list.")
        return
    largest_number = nums[0]
    second_largest_number = None

    for n in nums:
        if n > largest_number:
            second_largest_number = largest_number
            largest_number = n

        elif n < largest_number:
            if second_largest_number is None or n > second_largest_number:
                second_largest_number = n

    if second_largest_number is None:
        print("There is no second-largest distinct number.")
        return

    print(f"Second largest number is {second_largest_number}")


def remove_duplicates():
    nums = input("Enter elemnt seprarted by space : ").split()
    cleaned_nums = []
    for n in nums:
        if n not in cleaned_nums:
            cleaned_nums.append(n) 
    print("Cleaned list is : ", cleaned_nums)   


def separate_even_odd():
    try: 
        nums = [int(n) for n in input("Enter elements separated by space: ").split()]

        even_nums = []
        old_nums = []
        for i,n in enumerate(nums):
            if n % 2 == 0:
                even_nums.append(n)
            else:
                old_nums.append(n)
        print("even element list : ",even_nums)
        print("old element list : ",old_nums)
    except:
        print("something went wrong")




def find_common_values():
    list1 = input("Enter elemnt seprarted by space for list 1 : ").split()
    list2 = input("Enter elemnt seprarted by space for list 2 : ").split()
    common_list = []
    for i in list1:
        if i in list2 and i not in common_list:
            common_list.append(i)

def count_frequency():
    count = {}
    nums = input("Enter elemnt seprarted by space : ").split()
    if not nums:
        print("please enter an vaild list")
    for n in nums:
        if n in count:
            count[n] += 1
        else:
            count[n] =1 
    print(count)

def marks_dictionary():
    marks = {
        "Mayank": 85,
        "Rahul": 72,
        "Aman": 91,
        "Priya": 68
    }

    if not marks:
        print("Marks dictionary is empty.")
        return

    highest_scorer = max(marks, key=marks.get) # type: ignore
    lowest_scorer = min(marks, key=marks.get)  # type: ignore

    average = sum(marks.values()) / len(marks)

    print(f"Highest scorer: {highest_scorer} - {marks[highest_scorer]}")
    print(f"Lowest scorer: {lowest_scorer} - {marks[lowest_scorer]}")
    print(f"Average marks: {average:.2f}")
def main():
    print("========== Task 4: Lists and Dictionaries ==========")

    print("\n--- Largest and Smallest Element ---")
    largest_smallest_element([10, 5, 20, 2, 15])

    print("\n--- Second Largest Distinct Element ---")
    find_second_largest([10, 40, 20, 40, 30])

    print("\n--- Remove Duplicates ---")
    remove_duplicates()

    print("\n--- Separate Even and Odd ---")
    separate_even_odd()

    print("\n--- Common Values ---")
    find_common_values()

    print("\n--- Count Frequency ---")
    count_frequency()

    print("\n--- Marks Dictionary ---")
    marks_dictionary()


if __name__ == "__main__":
    main()