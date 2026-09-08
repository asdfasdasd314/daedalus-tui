"""Module-level resource read from multiple functions (LEGB aggregation)."""

bankroll = 100


def allocate():
    return bankroll * 0.1


def report():
    return bankroll
