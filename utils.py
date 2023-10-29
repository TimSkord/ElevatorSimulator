import bisect


def find_closest(sorted_list, val):
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


def has_larger(sorted_list, val):
    """Determines whether the sorted `sorted_list` has values greater than `val`."""
    pos = bisect.bisect_right(sorted_list, val)
    return pos < len(sorted_list)


def has_smaller(sorted_list, val):
    """Determines whether the sorted `sorted_list` has values less than `val`."""
    pos = bisect.bisect_left(sorted_list, val)
    return pos > 0
