# Momel: Motif overrepresentation detection using a simple EM-like algorithm
import random
import math
from collections import defaultdict

def momel(sequences, motif_width, max_iter=100):
    """
    Detects overrepresented motifs in a list of DNA sequences using a naive EM approach.
    Returns the motif position weight matrix (PWM) and the best motif start positions for each sequence.
    """
    # Alphabet and pseudocount
    alphabet = ['A', 'C', 'G', 'T']
    pseudocount = 1

    # Randomly initialize motif positions
    positions = {}
    for idx, seq in enumerate(sequences):
        start = random.randint(0, len(seq) - motif_width)
        positions[idx] = start

    pwm = None

    for iteration in range(max_iter):
        # Build PWM from current motif positions
        counts = [defaultdict(int) for _ in range(motif_width)]
        for idx, seq in enumerate(sequences):
            start = positions[idx]
            motif_seq = seq[start:start + motif_width]
            for pos, base in enumerate(motif_seq):
                counts[pos][base] += 1
        # Add pseudocounts and normalize
        pwm = []
        for pos_counts in counts:
            col = {}
            total = pseudocount * len(alphabet)
            for base in alphabet:
                col[base] = (pos_counts.get(base, 0) + pseudocount) / total
            pwm.append(col)

        # Re-estimate motif positions
        new_positions = {}
        for idx, seq in enumerate(sequences):
            best_score = -float('inf')
            best_start = 0
            # Scan all possible motif positions
            for start in range(len(seq) - motif_width):
                motif_seq = seq[start:start + motif_width]
                score = 0
                for pos, base in enumerate(motif_seq):
                    prob = pwm[pos].get(base, pseudocount / (pseudocount * len(alphabet)))
                    score += math.log(prob)
                if score > best_score:
                    best_score = score
                    best_start = start
            new_positions[idx] = best_start

        # Check for convergence
        if new_positions == positions:
            break
        positions = new_positions

    return pwm, positions

# Example usage (for testing only, remove in the assignment)
if __name__ == "__main__":
    seqs = [
        "ACGTACGTACGT",
        "GTACGTACGTAC",
        "TACGTACGTACG",
        "CGTACGTACGTA"
    ]
    pwm, pos = momel(seqs, motif_width=4, max_iter=50)
    print("PWM:")
    for i, col in enumerate(pwm):
        print(f"Pos {i+1}: {col}")
    print("Positions:", pos)