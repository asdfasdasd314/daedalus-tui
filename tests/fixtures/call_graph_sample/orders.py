"""Order-domain helpers that share naming and documentation vocabulary."""


def create_order() -> None:
    """Create a customer order and persist payment details."""
    # Kick off the order workflow.
    submit_order()
    save_order()


def submit_order() -> None:
    """Submit order payment to the processor."""
    # Finalize payment for the order.
    pass


def save_order() -> None:
    """Save order records to durable storage."""
    # Persist the completed order.
    pass
