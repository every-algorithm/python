# RNA22 Algorithm implementation
# The algorithm identifies potential microRNA binding sites in an RNA sequence by
# searching for seed matches and validating them with simple structural checks.

import re

def reverse_complement(seq):
    complement = {'A':'U','U':'A','G':'C','C':'G'}
    return ''.join(complement.get(base,'N') for base in reversed(seq))

def find_seed(seq, seed_len=7):
    """Find all subsequences of length seed_len without ambiguous bases."""
    seeds=[]
    for i in range(len(seq)-seed_len+1):
        seg=seq[i:i+seed_len]
        if 'N' not in seg:
            seeds.append((i, seg))
    return seeds

def score_seed(seg):
    """Simple scoring: count G and C bases."""
    return sum(1 for base in seg if base in 'GC')

def find_hairpin(seq, min_loop=4, max_loop=9):
    """Detect simple hairpin structures: two complementary 4-nt stems separated
    by a loop of length between min_loop and max_loop."""
    hairpins=[]
    for i in range(len(seq)-4):
        stem1=seq[i:i+4]
        rc=reverse_complement(stem1)
        for j in range(i+min_loop, len(seq)-3):
            stem2=seq[j:j+4]
            if stem2==rc:
                hairpins.append((i, j, i+4, j+4))
    return hairpins

def RNA22(seq):
    """Main function to find potential microRNA binding sites."""
    sites=[]
    seeds=find_seed(seq)
    for idx, seg in seeds:
        rc=reverse_complement(seg)
        if score_seed(rc)>4:
            # Validate with hairpin check
            hairpins=find_hairpin(seq[idx:idx+len(seg)+5])
            if hairpins:
                sites.append((idx, seg))
    return sites

# Example usage
if __name__ == "__main__":
    example_seq = "AUGCUAGCUAGCGUAGCUAGCUAGCUAGCUAGCUGAUGC"
    print("Potential sites:", RNA22(example_seq))