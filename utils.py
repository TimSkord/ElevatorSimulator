import bisect

from faker import Faker

fake = Faker()


def find_closest(sorted_list: list, val: int) -> int:
    """Finds the closest value to `val` in the sorted set `sorted_list`."""
    if not sorted_list:
        return 0

    pos = bisect.bisect_left(sorted_list, val)

    if pos == 0:
        return sorted_list[0]

    if pos == len(sorted_list):
        return sorted_list[-1]

    before = sorted_list[pos - 1]
    after = sorted_list[pos]

    if after - val < val - before:
        return after
    else:
        return before


def has_larger(sorted_list: list, val: int) -> int:
    """Determines whether the sorted `sorted_list` has values greater than `val`."""
    pos = bisect.bisect_right(sorted_list, val)
    return pos < len(sorted_list)


def has_smaller(sorted_list: list, val: int) -> int:
    """Determines whether the sorted `sorted_list` has values less than `val`."""
    pos = bisect.bisect_left(sorted_list, val)
    return pos > 0


def generate_full_name() -> str:
    """Generates a random passenger's full name"""
    return fake.name()


def set_elevator_for_passengers(passengers_list, elevator):
    """Sets up a specific elevator for passengers"""
    for passenger in passengers_list:
        passenger.set_elevator(elevator)
