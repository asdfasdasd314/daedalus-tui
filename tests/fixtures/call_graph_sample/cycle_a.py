from call_graph_sample.cycle_b import func_b


def func_a() -> None:
    func_b()
