from node import AtomSpaceNode


class DeterminantNode(AtomSpaceNode):
    results_2x2: list[int | None] = [None, None, None]
    """
    Store the results of the 2x2 matrix
    """

    matrix: list[list[int]]
    """
    Represents the matrix
    Example:
    [
     [1, 2, 3],
     [1, 2, 3],
     [1, 2, 3],
    ]
    """
