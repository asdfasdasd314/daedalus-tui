from call_graph_sample.b import beta
from call_graph_sample.orders import create_order
from call_graph_sample.ui import manage_ui


def alpha() -> None:
    """Entry helper that fans out into order and UI branches."""
    beta()
    create_order()
    manage_ui()
