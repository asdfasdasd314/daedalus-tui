"""Nested function LEGB plus nonlocal / global mutation cases."""

shared = 1


def outer():
    total = 10

    def inner():
        nonlocal total
        total += shared
        return total

    return inner()


def bump_shared():
    global shared
    shared += 1
    return shared
