from call_graph_sample.c import gamma


def beta() -> None:
    """Continue the sample call chain toward gamma."""
    gamma()
