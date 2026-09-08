"""Assignment lineage, augassign, attribute mutate, and unique call mapping."""

capital = 10_000


def calculate(x):
    return x * 2


def execute_trade(capital, price):
    risk = capital * 0.02
    size = risk / price
    amount = size
    amount -= 1
    return amount


def run_pipeline(price):
    risk_budget = capital * 0.02
    sized = calculate(capital)
    traded = execute_trade(capital, price)
    return risk_budget, sized, traded


class Portfolio:
    def __init__(self):
        self.capital = 5000

    def apply_cost(self, trade_cost):
        self.capital -= trade_cost
