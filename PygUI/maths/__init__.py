import math as _math


def within_rectangle(x: int, y: int, size: [4]) -> bool:
    """Returns whether inside a rectangle or not"""
    return size[0] <= x < size[0] + size[2] and size[1] <= y < size[1] + size[3]


def get_increase_list(new: list, old: list) -> [4]:
    """Takes in a list of four integers, increasing each index populated, by one."""
    if old[0] > 0:
        new[0] += 1
    else:
        new[0] = 0

    if old[1] > 0:
        new[1] += 1
    else:
        new[1] = 0

    if old[2] > 0:
        new[2] += 1
    else:
        new[2] = 0
    return new


def most(x: int or float, y: int or float) -> int or float:
    """Returns the highest value"""
    return x if x > y else y


def smallest(x: int or float, y: int or float) -> int or float:
    """Returns the smallest value"""
    return x if x < y else y


def most_from_list(array: [int or float]) -> int or float:
    """Returns largest value in an array"""
    array.sort()
    return array[-1]


def smallest_from_list(array: [int or float]) -> int or float:
    """Returns smallest value in an array"""
    array.sort()
    return array[0]


def most_list_index(array: [int or float]) -> int or float:
    """Returns the index of the biggest number"""
    temp = array[:]
    temp.sort()
    return array.index(temp[-1])


def smallest_list_index(array: [int or float]) -> int or float:
    """Returns the index of the smallest number"""
    temp = array[:]
    temp.sort()
    return array.index(temp[0])


def most_list_indexes(array: [int or float]):
    """Returns an array of the indices of the biggest number"""
    # TODO: complete


def smallest_list_indexes(array: [int] or [float]):
    """Returns an array of the indices of the smallest number"""
    # TODO: complete


def abc(a: int or float, b: int or float, c: int or float) -> [float] or None:
    if a == 0:
        return None
    else:
        d = b * b - 4 * a * c
        if d < 0:
            return None
        elif d == 0:
            e = -b / (2 * a)
            return [e]
        else:
            f = (-b + _math.sqrt(d)) / (2 * a)
            g = (-b - _math.sqrt(d)) / (2 * a)
            return [f, g]


print(abc(2, -1, 1))
