def square_digits(num: int):
    """
    For example, if we run 9119 through the function, 811181 will come out, because 92 is 81 and 12 is 1.
    Note: The function accepts an integer and returns an integer
    """
    if num <= 0:
        raise ValueError

    results = ""
    for i in str(num):
        sq = int(i)
        sq = sq * sq
        results = results + str(sq)

    return int(results)


import math


def is_square(num):
    if num < 0:
        return False
    if num == 0:
        return True

    root = math.sqrt(num)
    if root % 1 == 0:
        if int(root) * int(root) == num:
            return True
    return False


def open_or_senior(data):
    results = []
    for i, j in data:
        if i >= 55 and j > 7:
            results.append("Senior")
        else:
            results.append("Open")
    return results


def high_and_low(num):
    """
    In this little assignment you are given a string of space separated numbers,
    and have to return the highest and lowest number.
    high_and_low("1 2 3 4 5")  # return "5 1"
    """
    high = 0
    low = 0

    for i in num.split():
        # high and low cannot be 0 when starting
        if low == 0:
            low = int(i)
        elif high == 0:
            high = int(i)

        if int(i) > high:
            high = int(i)
        elif int(i) < low:
            low = int(i)

    return f"{high} {low}"


def create_phone_number(n):
    base = "".join([str(x) for x in n[:3]])
    middle = "".join([str(x) for x in n[3:6]])
    end = "".join([str(x) for x in n[6:]])

    return f"({base}) {middle}-{end}"


def DNA_strand(dna):
    out = ""
    for i in dna:
        if i == "A":
            out = out + "T"
        if i == "T":
            out = out + "A"
        if i == "G":
            out = out + "C"
        else:
            out = out + "G"
    return out


def dig_pow(n, p):
    check1 = 0
    num = [int(x) for x in str(n)]
    count = 0

    for i in num:
        data = i ** (p + count)
        count = count + 1
        check1 = check1 + data

    diff = int(check1 / n)

    if diff != 0:
        return diff
    else:
        return -1


dig_pow(89, 1)
dig_pow(92, 1)
dig_pow(695, 2)
dig_pow(46288, 3)
