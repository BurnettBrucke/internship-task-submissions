def returning1_to_10():
    numbers = iter(range(1, 11))
    for number in numbers:
        print(number)


# returning1_to_10()


def generate_evenupto50():
    for number in range(51):
        if number % 2 == 0:
            yield number


# for number in generate_evenupto50():
#     print(number)
import sys


def compare_size():
    number_list = list(range(1000000))
    number_gene = (number for number in range(1000000))

    print(f"memory used in storing 10m data: {sys.getsizeof(number_list)}")
    print(
        f"memory used in storing 10m data using generator: {sys.getsizeof(number_gene)}"
    )


compare_size()
