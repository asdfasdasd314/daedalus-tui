from call_graph_sample.cycle_a import func_a


def func_b() -> None:
    func_a()
