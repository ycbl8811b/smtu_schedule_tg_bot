from string import digits

def is_digit(string: str) -> bool:
    for ch in string:
        if not(ch in digits):
            return False
    return True


def is_list_elems_type(array: list, elems_type: type):
    return all(isinstance(elem, elems_type) for elem in array)