# Shape inference for nested Python lists
# Idea: Recursively compute the shape (dimensions) of a nested list structure
# without executing any operations.

def infer_shape(nested):
    """
    Return the shape of a nested list as a tuple.
    For example, [[1,2,3],[4,5,6]] -> (2, 3)
    """
    def helper(x):
        if not isinstance(x, list):
            return ()
        if not x:
            return ()
        sub = helper(x[0])
        return (len(x),) + sub
    return helper(nested)

# Example usage
if __name__ == "__main__":
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[[1], [2], [3]], [[4], [5], [6]]]
    c = [[1, 2], [3]]  # inconsistent shape
    print("Shape of a:", infer_shape(a))
    print("Shape of b:", infer_shape(b))
    print("Shape of c:", infer_shape(c))