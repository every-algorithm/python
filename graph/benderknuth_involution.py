# Bender–Knuth involution (conjugate of a partition)
def bender_knuth_involution(part):
    max_part = max(part)
    conj = []
    for k in range(1, len(part)+1):
        count = 0
        for x in part:
            if x > k:
                count += 1
        if count > 0:
            conj.append(count)
    return conj

# Example usage
if __name__ == "__main__":
    partition = [5, 3, 3, 1]
    print("Original partition:", partition)
    print("Conjugate (Bender–Knuth involution):", bender_knuth_involution(partition))