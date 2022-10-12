import pytest


def split_strings(s):
    """
    Complete the solution so that it splits the string into pairs of two characters.
    If the string contains an odd number of characters then it should replace the
    missing second character of the final pair with an underscore ('_').
    """
    # if s is empty
    if len(s) == 0:
        return []
    # if s is odd
    if len(s) % 2 != 0:
        s = s + "_"

    output = []
    while s:
        output.append(s[:2])
        s = s[2:]
    return output


@pytest.mark.parametrize(
    ("test", "excepted"),
    (
        (("asdfadsf", ["as", "df", "ad", "sf"])),
        (("asdfads", ["as", "df", "ad", "s_"])),
        (("", [])),
        (("x", ["x_"])),
    ),
)
def test_split_strings(test, excepted):
    assert split_strings(test) == excepted


def count_bits(n):
    """
    Write a function that takes an integer as input, and returns the
    number of bits that are equal to one in the binary representation
    of that number. You can guarantee that input is non-negative.
    Example: The binary representation of 1234 is 10011010010, so the
    function should return 5 in this case
    """
    return bin(n).count("1")


@pytest.mark.parametrize(
    ("test", "excepted"),
    (
        ((0, 0)),
        ((4, 1)),
        ((7, 3)),
        ((9, 2)),
        ((10, 2)),
    ),
)
def test_count_bits(test, excepted):
    assert count_bits(test) == excepted


def queue_time(customers, n):
    l = [0] * n
    for i in customers:
        l[l.index(min(l))] += i
    return max(l)


def find_it(seq):
    """
    Given an array of integers, find the one that appears an odd number of times.
    There will always be only one integer that appears an odd number of times.

    Examples
    [7] should return 7, because it occurs 1 time (which is odd).
    [0] should return 0, because it occurs 1 time (which is odd).
    [1,1,2] should return 2, because it occurs 1 time (which is odd).
    [0,1,0,1,0] should return 0, because it occurs 3 times (which is odd).
    [1,2,2,3,3,3,4,3,3,3,2,2,1] should return 4, because it appears 1 time (which is odd).
    """
    seq_set = set(seq)
    output = 0
    for i in seq_set:
        occurences = seq.count(i)
        print(f"{i} occured {occurences} times.")
        if occurences % 2 != 0:
            output = i
    print(f"output: {output}\n")
    return output


def order(sentence):
    """
    Your task is to sort a given string. Each word in the string will contain a single number.
    This number is the position the word should have in the result.
    Note: Numbers can be from 1 to 9. So 1 will be the first word (not 0).
    If the input string is empty, return an empty string. The words in the input String will
    only contain valid consecutive numbers.
    """
    if len(sentence) == 0:
        return sentence
    size = len(sentence) - 1

    output = ["" * size]
    sentence = sentence.split()
    for i in sentence:
        for x in i:
            if x.isnumeric():
                output.insert(int(x) - 1, i)

    return " ".join([i for i in output if i])


print(order("4of Fo1r pe6ople g3ood th5e the2"))
"""
"is2 Thi1s T4est 3a"  -->  "Thi1s is2 3a T4est"
"4of Fo1r pe6ople g3ood th5e the2"  -->  "Fo1r the2 g3ood 4of th5e pe6ople"
""  -->  ""
"""
