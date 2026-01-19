"""
Docstring for p1
"""


def evenorodd(a):
    """
    Docstring for evenorodd
    """
    if a & 1 == 0:
        return "even"
    return "odd"


if __name__ == "__main__":
    print(evenorodd(int(input())))
