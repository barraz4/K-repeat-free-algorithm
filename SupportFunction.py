import math
import random

min_n = 13404  # len(encoding_block) = k'-1. this is the min n that satisfy this condition
n = 0
logn = 0
loglogn = 0
marker = "0"
k_tag = 0
k = 0
original_w = ""


def find_min_n_from_input_sequence(input_sequence_length: int) -> int:
    def inequality_function(n, input_length):
        if n <= 1:
            return float('inf')  # Avoid domain error for loglog
        return n - (4 * math.log2(math.log2(float(n))) + 3) - input_length

    # Initial guess for n, +4 to match +3 and min of loglogn that can be 1
    n = input_sequence_length + 4

    while True:
        diff = inequality_function(n, input_sequence_length)
        if diff < 0:
            n += int(-diff) + 1  # add diff to n for faster convergence
        else:
            return n


def update_n(w: str, from_w: bool):
    global n, logn, loglogn, marker, k_tag, k, original_w
    n = len(w) if not from_w else find_min_n_from_input_sequence(len(w))
    assert n != 0
    logn = math.log2(n)
    loglogn = math.log2(math.log2(n))
    k_tag = logn + 2 * loglogn + 5
    k = k_tag + 8 * loglogn + 5

    logn = math.floor(logn)
    loglogn = math.floor(loglogn)
    k_tag = math.floor(k_tag)
    k = math.floor(k)
    marker = "0" * (2 * loglogn)
    original_w = w if from_w else original_w


def generate_input_sequence(length=13404):
    return ''.join(random.choice('01') for _ in range(length))


def validate_indices(indices: tuple) -> list:
    assert len(indices) == 2
    i, j = min(indices), max(indices)
    return [i, j]


def get_n():
    assert n != 0
    return n


def sequence_validation(w: str) -> str:
    """
    Ensure no sequence of 0's of length 2log(log(n)) appears.
    if appear change the 2log(log(n)) zero to 2
    """
    len_w = len(w)
    index = w.find(marker)
    while index != -1:
        w = w[:index + len(marker) - 1] + '2' + w[index + len(marker):]
        index = w.find(marker)
    assert len(w) == len_w
    return w


def remove_sequence_validation(w: str) -> str:
    """
    change 2 into zero to remove sequence_validation() action
    """
    return w.replace('2', '0')


def fi(i: int) -> str:
    """
    return i in binary repesenataoin with log(n)+1 bits.
    need to apply sequence_validation to not append a marker
    """
    binary_rep = bin(i)[2:].zfill(logn + 1)  # [2:] slice 0b prefix. zfill will pad to log(n)+1 length
    return sequence_validation(binary_rep)


# ----- User Interface ------
def get_valid_input(list_of_values_to_choose_from, title) -> int:
    range_as_strings = [str(i) for i in range(1, len(list_of_values_to_choose_from) + 1)]
    while True:
        print(title)
        for i, val in enumerate(list_of_values_to_choose_from):
            print(f"{i + 1}. {val}")
        sel = input("Enter the number of your choice: ")
        if sel in range_as_strings:
            select = int(sel)
            break
        print(f"\nInvalid choice! \nPlease enter a number between {1} and {len(list_of_values_to_choose_from)}\n\n")
    print("")
    return select
