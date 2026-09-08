"""Second helper with the same simple name as ambiguous_a.helper."""


def helper(value):
    return value * 3


def run_other(token):
    return helper(token)
