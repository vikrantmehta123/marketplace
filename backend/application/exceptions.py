class CancellationNotPossibleError(Exception):
    """Exception class for when the order is already dispatched and the buyer tries to cancel"""
    pass