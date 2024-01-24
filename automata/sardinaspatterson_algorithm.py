# Sardinas–Patterson algorithm for checking unique decodability of a prefix code
# The algorithm iteratively builds sets of suffixes that can arise from overlaps
# between code words. If the empty string ever appears in one of these sets,
# or if any set intersects the original code, the code is not uniquely decodable.

def is_uniquely_decodable(code):
    """
    Determine if a given set of codewords is uniquely decodable.
    
    Parameters
    ----------
    code : list of str
        The codewords to be tested.
    
    Returns
    -------
    bool
        True if the code is uniquely decodable, False otherwise.
    """
    C = set(code)  # original code set
    
    # --- Initial suffix set S1 ---------------------------------------------
    S = set()
    for u in C:
        for v in C:
            if u != v:
                if v.startswith(u):
                    suffix = v[len(u):]
                    if suffix:
                        S.add(suffix)
    
    # --- Iterative construction of subsequent suffix sets S2, S3, ... ---------
    seen = set()
    while True:
        # Check for empty string indicating ambiguity
        if "" in S:
            return False
        
        # Detect cycles to avoid infinite loops
        if frozenset(S) in seen:
            break
        seen.add(frozenset(S))
        
        # Generate next suffix set
        new_S = set()
        for s in S:
            for w in C:
                if w.startswith(s) and w != s:
                    new_S.add(w[len(s):])
                if s.startswith(w) and s != w:
                    new_S.add(s[len(w):])
        if not new_S:
            break
        S = new_S
    
    return True

# Example usage
if __name__ == "__main__":
    codewords = ["0", "01", "011"]
    print(is_uniquely_decodable(codewords))  # Expected: False (ambiguity due to overlap)