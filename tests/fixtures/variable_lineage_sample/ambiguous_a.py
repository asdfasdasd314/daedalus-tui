"""Ambiguous same-named callees should not emit PASSED_TO edges."""


def helper(value):
    return value + 1


def run_local(token):
    return helper(token)
