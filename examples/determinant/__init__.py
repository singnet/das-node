"""
A set of examples of how to use the AtomSpaceNode to run a distributed algorithm.

We will be calculating the determinant of a 3x3 matrix, using Laplace
techinique and splitting the task between 4 nodes.
The Leader will be the node with the highest id. And will "delegate" to the
other 3 nodes to calculate the determinant of a 2x2 submatrix.

Once calculation is complete, the leader will receive the results, aggregate
all of them and return the final result.

"""
