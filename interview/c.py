"""
[2, 4, 0, 100, 4, 11, 2602, 36]
Should return: 11 (the only odd number)
"""


def find_outlier(integers):
    tmp1 = []
    tmp2 = []
    for i in integers:
        if i % 2 == 0:
            tmp1.append(i)
        else:
            tmp2.append(i)

    if len(tmp1) == 1:
        return tmp1[0]
    else:
        return tmp2[0]


"""
Implement a pseudo-encryption algorithm which given a string S and an integer N concatenates 
all the odd-indexed characters of S with all the even-indexed characters of S, this process should be repeated N times.

Examples:

encrypt("012345", 1)  =>  "135024"
encrypt("012345", 2)  =>  "135024"  ->  "304152"
encrypt("012345", 3)  =>  "135024"  ->  "304152"  ->  "012345"

encrypt("01234", 1)  =>  "13024"
encrypt("01234", 2)  =>  "13024"  ->  "32104"
encrypt("01234", 3)  =>  "13024"  ->  "32104"  ->  "20314"
Together with the encryption function, you should also implement a decryption function which reverses the process.

If the string S is an empty value or the integer N is not positive, return the first argument without changes.
"""


def decrypt(encrypted_text, n):
    if encrypted_text == "" or encrypted_text == None or n <= 0:
        return encrypted_text

    out = ""
    tmp = ""
    for i, num in enumerate(encrypted_text):
        if int(i) % 2:
            tmp = tmp + num
        else:
            out = out + num
    print(tmp + out)


def encrypt(text, n):
    if text == "" or text == None or n <= 0:
        return text

    for _ in range(n):
        out = ""
        tmp = ""
        for i, num in enumerate(text):
            if int(i) % 2:
                out = out + num
            else:
                tmp = tmp + num

        text = out + tmp
        print(text)


# encrypt("This is a test!", 1)
# decrypt("hskt svr neetn!Ti aai eyitrsig", 1)


def array_diff(a, b):
    set_a = set(a)
    set_b = set(b)
    matching = set_a.intersection(set_b)
    for i in matching:
        while i in a:
            a.remove(i)

    return a


# array_diff([1,2,2,2,3],[2]) == [1,3]
# array_diff([1,2,3], [1, 2]) == [3]

# array_diff([1,2,2,2,3],[2])
array_diff([1, 2, 3], [1, 2])
print(array_diff([1, 2, 2], [2]))
